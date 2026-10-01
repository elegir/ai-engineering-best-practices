"""llm_call_skeleton.py — the ONE module in the repo that talks to a model vendor.

Copy to <repo>/src/<package>/llm.py. Replace <<MODEL>>, <<MAX_OUTPUT_TOKENS>>, <<TIMEOUT_S>>.
Nothing else in the repo imports the vendor SDK; everything calls `call()` (or `stream()`).

What this buys you (see principles/10-llm-api-fundamentals.md):
  * one place for the model name, limits, timeout, retries      -> switching vendor = this file + config
  * the request is the agentic shape: system + typed items + tools -> works for one call or a loop
  * usage is logged per call, INCLUDING cached input tokens        -> you can see whether prompt caching hits
  * static parts (system, tools) are sent first, dynamic last      -> prompt caching can hit
  * errors are returned as a result, not raised into handlers      -> callers decide; nothing crashes mid-loop

Anthropic Messages API is shown. OpenAI Responses adapter: see `_call_openai` at the bottom —
same shape (instructions + `input` items + tools -> output items), different field names.
Requires: pip install anthropic   (or openai)
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any

import anthropic

log = logging.getLogger("llm")

MODEL = "<<MODEL>>"                  # one place. Tier policy: principles/08-model-selection.md
MAX_OUTPUT_TOKENS = <<MAX_OUTPUT_TOKENS>>   # e.g. 1024 for a classifier, 8192 for a writer
TIMEOUT_S = <<TIMEOUT_S>>            # e.g. 60; a call without a timeout is an outage waiting
MAX_RETRIES = 2                      # on rate limit / overload only; never retry a 4xx you caused.
                                     # In production, ONE retry owner: if a gateway/router retries (practices/llm-gateway/), set this to 0.

_client = anthropic.Anthropic(timeout=TIMEOUT_S, max_retries=0)  # we handle retries ourselves


def client() -> anthropic.Anthropic:
    """The ONE vendor client (assertion 1). Other modules that need the raw SDK — e.g. the structured-outputs
    module ../structured-outputs/structured_call.py — import this accessor instead of instantiating their own."""
    return _client


@dataclass
class Result:
    """What every caller gets back. `error` is set instead of raising."""
    text: str = ""
    items: list[dict[str, Any]] = field(default_factory=list)   # raw output blocks (text, tool_use, thinking)
    stop_reason: str = ""
    usage: dict[str, int] = field(default_factory=dict)
    error: str | None = None


def call(
    system: str | list[dict[str, Any]],
    items: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None = None,
    *,
    thinking_budget: int | None = None,   # reasoning models: set a budget instead of "step 1, step 2" in the prompt
    model: str = MODEL,
) -> Result:
    """One model call.

    system : the static prompt (prompts/<feature>/system.md rendered), cache-controlled below
    items  : the typed item list you OWN — user/assistant messages, tool_use, tool_result — resent each turn
    tools  : tool definitions (name, description, input_schema); the description is prompt, write it as such
    Keep `system` and `tools` identical between turns: they are the cached prefix. Put anything that
    varies per request (date, user, session) at the END of `system` or in the first user item.
    """
    # Cache control: mark the end of the static prefix. (Anthropic: explicit breakpoint; OpenAI: automatic on a stable prefix.)
    if isinstance(system, str):
        system = [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]

    kwargs: dict[str, Any] = dict(model=model, max_tokens=MAX_OUTPUT_TOKENS, system=system, messages=items)
    if tools:
        kwargs["tools"] = tools
    if thinking_budget:
        # The API rejects the call unless max_tokens > budget_tokens: the budget is part of the output.
        if thinking_budget >= MAX_OUTPUT_TOKENS:
            return Result(error=f"thinking_budget {thinking_budget} must be < MAX_OUTPUT_TOKENS {MAX_OUTPUT_TOKENS}")
        kwargs["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}

    for attempt in range(MAX_RETRIES + 1):
        t0 = time.monotonic()
        try:
            resp = _client.messages.create(**kwargs)
        except (anthropic.RateLimitError, anthropic.APIStatusError) as e:
            status = getattr(e, "status_code", 0)
            if status in (429, 529, 500, 502, 503) and attempt < MAX_RETRIES:
                time.sleep(2 ** attempt)
                continue
            return Result(error=f"{type(e).__name__}: {e}")
        except anthropic.APITimeoutError:
            return Result(error=f"timeout after {TIMEOUT_S}s")

        usage = {
            "input": resp.usage.input_tokens,
            "output": resp.usage.output_tokens,
            "cache_read": getattr(resp.usage, "cache_read_input_tokens", 0) or 0,
            "cache_write": getattr(resp.usage, "cache_creation_input_tokens", 0) or 0,
            "ms": int((time.monotonic() - t0) * 1000),
        }
        # This log line is how you verify caching and cost per feature. Keep it.
        log.info("llm model=%s stop=%s attempt=%d usage=%s", model, resp.stop_reason, attempt, usage)  # attempt = retry count (assertion 4)

        # `stop_reason` values `refusal` and `max_tokens` are NOT parse errors: a structured call returns them as typed
        # branches — see ../structured-outputs/structured_call.py (practices/structured-outputs/, 2026-10-01).
        blocks = [b.model_dump() for b in resp.content]
        text = "".join(b["text"] for b in blocks if b.get("type") == "text")
        return Result(text=text, items=blocks, stop_reason=resp.stop_reason, usage=usage)

    return Result(error="unreachable")


def assistant_item(result: Result) -> dict[str, Any]:
    """Append the model's turn to your item list before running tools / calling again."""
    return {"role": "assistant", "content": result.items}


def tool_result_item(tool_use_id: str, content: str, is_error: bool = False) -> dict[str, Any]:
    """Append a tool result. Errors go back as TEXT so the model can self-correct (principle 21)."""
    return {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_use_id,
                                          "content": content, "is_error": is_error}]}


# --- OpenAI Responses adapter (sketch; same shape, different names) -----------------------
# from openai import OpenAI
# def _call_openai(instructions, items, tools=None, *, reasoning_effort=None, model=MODEL) -> Result:
#     resp = OpenAI(timeout=TIMEOUT_S).responses.create(
#         model=model, instructions=instructions, input=items, tools=tools or [],
#         reasoning={"effort": reasoning_effort} if reasoning_effort else None,
#         max_output_tokens=MAX_OUTPUT_TOKENS,
#         # store=False + include=["reasoning.encrypted_content"] for stateless / zero-data-retention,
#         # or previous_response_id=... to let the server keep the chain (lock-in: write it down).
#     )
#     usage = {"input": resp.usage.input_tokens, "output": resp.usage.output_tokens,
#              "cache_read": resp.usage.input_tokens_details.cached_tokens}
#     return Result(text=resp.output_text, items=[o.model_dump() for o in resp.output],
#                   stop_reason=resp.status, usage=usage)


if __name__ == "__main__":  # `python3 llm_call_skeleton.py --demo`: builds and prints the request shape without calling the API
    import json, sys
    if "--demo" in sys.argv:
        demo = {"model": MODEL, "max_tokens": MAX_OUTPUT_TOKENS, "retry_owner": "this module (max_retries=0 on the client)",
                "system": [{"type": "text", "text": "<static system prompt — cached>", "cache_control": {"type": "ephemeral"}}],
                "messages": [{"role": "user", "content": "<dynamic content last>"}]}
        print(json.dumps(demo, indent=1)); print("usage fields logged per call: input_tokens output_tokens cache_read_input_tokens cache_creation_input_tokens latency_ms attempt")
    else:
        print("usage: python3 llm_call_skeleton.py --demo  (prints the request shape; the real call is call())")
