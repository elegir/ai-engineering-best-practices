"""structured_call.py — the ONE place where a model output becomes a typed object.

Copy to <repo>/src/<package>/llm_structured.py, next to the client module of practices/llm-api-calls/
(llm.py). Replace <<MODEL>>, <<MAX_OUTPUT_TOKENS>>. The vendor client is NOT created here: it is imported
from llm.py's `client()` accessor, so that exactly one module instantiates the SDK (llm-api-calls assertion 1).
Nothing else in the repo parses model output: every call site asks `structured()` for a typed object and
gets a `Result` with one of FIVE branches — ok / refusal / truncated / invalid / error — never a JSON exception.

What this buys you (principles/13-structured-outputs-and-guardrails.md):
  * the provider guarantees the SHAPE (constrained decoding)      -> no json.loads, no regex, no schema retries
  * validators in code guarantee the MEANING (invariants)         -> totals add up, quotes exist, ids resolve
  * one bounded re-ask that carries the validator's message        -> one owner, cap of one, counted in the log
  * refusal and truncation are typed results, not parse errors    -> callers decide; nothing crashes mid-loop
  * schema version + attempt logged beside the prompt version      -> a schema change is a versioned change

Why `messages.create` + `output_config` and not the SDK's `messages.parse(output_format=Model)`: `parse()`
validates eagerly inside the SDK call, so a validator failure, a truncated object or a refusal-with-text would
raise there — outside the try/except that owns the re-ask — and the truncated/refusal branches would be
unreachable. With `create` the module checks `stop_reason` FIRST and runs the Pydantic validators ITSELF, in
one place. (`create` also sends the schema exactly as Pydantic emits it — no SDK transform — so `extra="forbid"`
must be on every model.) API shape read from the Anthropic structured-outputs page on 2026-10-01.

Python idioms, not required (decision 0005 §3): Pydantic as schema generator and validator; the `Result`
dataclass; the generic `Maybe[T]`. Any stack satisfies the contract by sending a JSON Schema, checking the stop
reason before parsing, and keeping the five branches. OpenAI Responses adapter sketched at the bottom.
Requires: pip install anthropic pydantic   (anthropic is imported only through llm.py)
"""
from __future__ import annotations

import json
import logging
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from .llm import client  # the ONE vendor client (practices/llm-api-calls/llm_call_skeleton.py -> llm.py)

log = logging.getLogger("llm.structured")

MODEL = "<<MODEL>>"                          # one place; registry/tier policy: principles/08-model-selection.md
MAX_OUTPUT_TOKENS = <<MAX_OUTPUT_TOKENS>>   # a truncated object is NOT valid JSON: size this for the largest expected object
MAX_REASKS = 1          # Liu (2024): "one retry… basically enough". The re-ask has ONE owner: this module.
                        # If a library (Instructor, Pydantic AI) also re-asks, set its retries to 0 — never two layers.
TRANSPORT_ERRORS = ("RateLimitError", "APIStatusError", "APITimeoutError", "APIConnectionError")  # anthropic.* names; llm.py owns transport retries

T = TypeVar("T", bound=BaseModel)


# --- 1. The schema is a prompt (schema-design-rules.md) ------------------------------------------
class StrictModel(BaseModel):
    """Base for every output schema: closed object, every key required, optionals as `X | None` with no default."""
    model_config = ConfigDict(extra="forbid")   # -> additionalProperties: false (JSON Schema's default is "the opposite of what developers want" — Pokrass)


class LineItem(StrictModel):
    description: str = Field(description="The item as printed on the receipt, verbatim.")
    quantity: int = Field(description="Units bought; 1 if not printed.")
    unit_price: float = Field(description="Price per unit in the receipt's currency.")


class Receipt(StrictModel):
    """Example schema. Field descriptions say HOW, the system prompt says WHEN; descriptive key names help but are a habit, not an official recommendation."""
    reasoning: str = Field(description="One or two sentences on how the total was reconciled. Comes FIRST on purpose: the model reads what it already wrote.")
    merchant: str
    currency: Literal["USD", "MXN", "EUR", "unknown"] = Field(description="'unknown' is the out — never force a match.")
    items: list[LineItem]
    total: float
    notes: str | None = Field(description="Optional = nullable, still a REQUIRED key (no default, or Pydantic drops it from `required`).")

    @field_validator("total")
    @classmethod
    def total_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("total must be greater than 0 — re-read the amount printed as TOTAL")   # message names field + rule
        return v

    @model_validator(mode="after")
    def items_add_up(self) -> "Receipt":
        s = round(sum(i.quantity * i.unit_price for i in self.items), 2)
        if abs(s - round(self.total, 2)) > 0.01:
            # The invariant the grammar cannot express (Liu 2023). The message is the re-ask prompt: say what is wrong AND what to do.
            raise ValueError(f"items sum to {s} but total is {self.total}; fix the quantities, unit prices or the total so they agree")
        return self


class Maybe(StrictModel, Generic[T]):
    """The 'Maybe' shape (Liu 2023): result-or-explanation instead of a sentinel string like I DON'T KNOW."""
    result: T | None
    error: bool
    error_message: str | None


# --- 2. The typed result: five branches, never an exception ---------------------------------------
Branch = Literal["ok", "refusal", "truncated", "invalid", "error"]


@dataclass
class Result(Generic[T]):
    branch: Branch
    value: T | None = None
    message: str = ""                    # validator message / refusal note / provider error
    attempts: int = 0                    # 1 = first call; 2 = after one re-ask
    schema_version: str = ""
    usage: dict[str, int] = field(default_factory=dict)
    raw: str = ""                        # the text the provider returned (for the trace; redact before storing if personal)

    @property
    def ok(self) -> bool:
        return self.branch == "ok"


# --- 3. The call --------------------------------------------------------------------------------------
def structured(
    schema: type[T],
    system: str | list[dict[str, Any]],
    items: list[dict[str, Any]],
    *,
    schema_version: str,                 # e.g. "receipt-v3"; bump it with every schema change (it also breaks the prompt cache)
    prompt_version: str = "",            # the header `version:` of prompts/<feature>/system.md
    model: str = MODEL,
) -> Result[T]:
    """One structured call: provider-constrained shape, code-validated meaning, one bounded re-ask.

    schema : a Pydantic model (closed, all keys required, nullable optionals). Its JSON Schema goes to the API.
    system : the static prompt — identical between calls so the cache hits (practices/llm-api-calls/).
    items  : the typed item list you OWN. The re-ask APPENDS to a copy of it; the caller's list is untouched.
    Order inside the loop: transport error -> `error`; stop_reason refusal -> `refusal`; stop_reason max_tokens ->
    `truncated`; then parse + validate -> `ok`, or ValidationError -> one re-ask -> `invalid`.
    """
    if isinstance(system, str):
        system = [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
    output_config = {"format": {"type": "json_schema", "schema": schema.model_json_schema()}}
    convo = list(items)
    usage_total: dict[str, int] = {"input": 0, "output": 0, "cache_read": 0, "ms": 0}

    for attempt in range(1, MAX_REASKS + 2):          # 1 first call + MAX_REASKS re-asks
        t0 = time.monotonic()
        try:
            resp = client().messages.create(
                model=model, max_tokens=MAX_OUTPUT_TOKENS, system=system, messages=convo, output_config=output_config,
            )
        except Exception as e:                            # noqa: BLE001 — classified by name so this module never imports the SDK
            if type(e).__name__ not in TRANSPORT_ERRORS:
                raise
            # Transport errors are llm.py's / the gateway's business (one owner of retries). Here they are a branch.
            _log("error", model, schema_version, prompt_version, attempt, usage_total, str(e))
            return Result("error", message=f"{type(e).__name__}: {e}", attempts=attempt, schema_version=schema_version, usage=usage_total)

        usage_total["input"] += getattr(resp.usage, "input_tokens", 0) or 0
        usage_total["output"] += getattr(resp.usage, "output_tokens", 0) or 0
        usage_total["cache_read"] += getattr(resp.usage, "cache_read_input_tokens", 0) or 0
        usage_total["ms"] += int((time.monotonic() - t0) * 1000)
        raw = "".join(getattr(b, "text", "") or "" for b in resp.content)

        # Branch: refusal — HTTP 200, billed, no object. Not a parse error. (Anthropic docs 2026-10-01; Pokrass: "there's no error code for that")
        if resp.stop_reason == "refusal":
            _log("refusal", model, schema_version, prompt_version, attempt, usage_total)
            return Result("refusal", message="model refused to produce the object", attempts=attempt, schema_version=schema_version, usage=usage_total, raw=raw)

        # Branch: truncated — the object was cut at max_tokens; the JSON is incomplete. Raise MAX_OUTPUT_TOKENS, do not re-ask.
        if resp.stop_reason == "max_tokens":
            _log("truncated", model, schema_version, prompt_version, attempt, usage_total)
            return Result("truncated", message=f"output hit max_tokens={MAX_OUTPUT_TOKENS}; raise it for this schema", attempts=attempt, schema_version=schema_version, usage=usage_total, raw=raw)

        # Shape is guaranteed by the provider; MEANING is checked here, by the Pydantic validators, in this one place.
        try:
            value: T = schema.model_validate_json(raw)
        except ValidationError as e:
            msg = _message(e)
            _log("invalid", model, schema_version, prompt_version, attempt, usage_total, msg)
            if attempt > MAX_REASKS:
                return Result("invalid", message=msg, attempts=attempt, schema_version=schema_version, usage=usage_total, raw=raw)
            # The re-ask: the model's own output goes back as the assistant turn, the validator's message as the next user turn.
            # "It is the error message that is part of the prompt but conditionally added" (Liu). Nothing else changes.
            convo = convo + [
                {"role": "assistant", "content": raw},
                {"role": "user", "content": f"The previous answer did not pass validation: {msg}. Return the corrected object only."},
            ]
            continue

        _log("ok", model, schema_version, prompt_version, attempt, usage_total)
        return Result("ok", value=value, attempts=attempt, schema_version=schema_version, usage=usage_total, raw=raw)

    return Result("error", message="unreachable", schema_version=schema_version)


def _message(e: ValidationError) -> str:
    """Turn a ValidationError into one informative line: field → rule. This string IS the re-ask prompt; keep it specific."""
    parts = []
    for err in e.errors():
        loc = ".".join(str(x) for x in err.get("loc", ())) or "object"
        parts.append(f"{loc}: {err.get('msg', 'invalid')}")
    return "; ".join(parts)


def _log(branch: str, model: str, schema_version: str, prompt_version: str, attempt: int, usage: dict[str, int], msg: str = "") -> None:
    # One line per call, aggregatable: the schema version sits beside the prompt version (assertion 10), the attempt counts re-asks (assertion 4).
    log.info("llm.structured branch=%s model=%s schema=%s prompt=%s attempt=%d usage=%s msg=%s",
             branch, model, schema_version, prompt_version, attempt, json.dumps(usage), msg[:200])


# --- OpenAI Responses adapter (sketch; same contract, different names) -----------------------------
# resp = client().responses.create(model=model, instructions=system_text, input=convo, max_output_tokens=MAX_OUTPUT_TOKENS,
#                                  text={"format": {"type": "json_schema", "name": schema.__name__, "strict": True,
#                                                   "schema": schema.model_json_schema()}})
# truncated: resp.status == "incomplete" and resp.incomplete_details.reason == "max_output_tokens"
# refusal:   an output item of type "refusal" (the launch design: a field, not a 4xx — Pokrass 2024-09)
# then schema.model_validate_json(resp.output_text) inside the same try/except that drives the re-ask.
# Both vendors: the schema must be a closed object with every key required; see schema-design-rules.md for the dated limits.


# --- strict tool use: the same guarantee for tool ARGUMENTS (Anthropic docs 2026-10-01) ---------------
def strict_tool(name: str, description: str, schema: type[BaseModel]) -> dict[str, Any]:
    """A tool definition whose arguments are constrained to the schema: no hallucinated tool names or malformed arguments."""
    return {"name": name, "description": description, "strict": True, "input_schema": schema.model_json_schema()}


if __name__ == "__main__":   # `python3 -m <package>.llm_structured --demo`: prints the request shape and the five branches without calling the API
    if "--demo" in sys.argv:
        demo = {
            "model": MODEL, "max_tokens": MAX_OUTPUT_TOKENS, "reask_owner": "this module (MAX_REASKS=1; library retries = 0)",
            "client": "imported from llm.py (one vendor client per repo)",
            "system": [{"type": "text", "text": "<static system prompt — cached>", "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": "<the receipt text — dynamic content last>"}],
            "output_config": {"format": {"type": "json_schema", "schema": Receipt.model_json_schema()}},
            "or_strict_tool": strict_tool("record_receipt", "Store a parsed receipt (write).", Receipt),
        }
        print(json.dumps(demo, indent=1))
        print("result branches (five): ok | refusal (stop_reason=refusal) | truncated (stop_reason=max_tokens) | invalid (validator message after 1 re-ask) | error (transport)")
        print("logged per call: branch model schema_version prompt_version attempt input output cache_read ms msg")
    else:
        print("usage: python3 -m <package>.llm_structured --demo  (prints the request shape; the real call is structured())")
