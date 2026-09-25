"""agent-loop-skeleton.py — the minimal agent: a model calling tools in a loop.

Copy to <repo>/src/<feature>/agent_loop.py. Replace <<MODEL>>, TOOLS and MAX_ITERATIONS.
Anthropic Messages API is shown; the loop shape is identical for OpenAI / Gemini / any framework:
  call the model -> if it asked for tools, run them and append the results -> repeat -> stop when no tool call.

Design rules baked in (see principles/21-agent-design-and-tools.md):
  * tools are plain functions with a full docstring: the docstring IS the prompt for that tool
  * tools RETURN errors as text (never raise): the model reads the error and self-corrects
  * every run is bounded: MAX_ITERATIONS and per-tool limits
  * debug=True prints exactly what the model chose (parameters) and what it got back (results),
    so you can "think like your agent" before touching the prompt
Requires: pip install anthropic
"""
from __future__ import annotations
import json
from typing import Any, Callable

import anthropic

MODEL = "<<MODEL>>"            # e.g. the current Sonnet-tier model id; see principles/08-model-selection.md
MAX_ITERATIONS = 12            # hard cap: an agent without a cap is a bill without a ceiling
MAX_TOOL_RESULT_CHARS = 8000   # truncate tool output so one call cannot flood the context

SYSTEM_PROMPT = """<<One paragraph: the goal, the constraints, what ideal behaviour looks like,
when to stop and answer, when to say you cannot do it.>>"""

# ---------------------------------------------------------------------------
# Tools: plain functions. Name, docstring and parameter names are what the model sees.
# ---------------------------------------------------------------------------

def get_order(order_id: str) -> str:
    """Return everything a support agent would see on the order page for ORDER_ID:
    status, items, amounts, shipping events and the customer's last three messages, as markdown.
    Use this before answering any question about a specific order. Returns an error message
    (not an exception) if the order does not exist."""
    # <<implementation>>  — shape the return like the UI, not like three API endpoints
    return "error: order 123 not found"

TOOLS: dict[str, Callable[..., str]] = {
    "get_order": get_order,
}

def _schema_for(fn: Callable[..., str]) -> dict[str, Any]:
    """Build the JSON schema the model sees from the function signature + docstring.
    Keep it simple: strings unless you need otherwise. Replace with pydantic if you prefer."""
    import inspect
    sig = inspect.signature(fn)
    props, required = {}, []
    for name, param in sig.parameters.items():
        typ = "integer" if param.annotation is int else "string"
        props[name] = {"type": typ, "description": f"<<describe {name}>>"}
        if param.default is inspect.Parameter.empty:
            required.append(name)
    return {
        "name": fn.__name__,
        "description": inspect.getdoc(fn) or "<<MISSING DOCSTRING — fix before shipping>>",
        "input_schema": {"type": "object", "properties": props, "required": required},
    }

TOOL_SCHEMAS = [_schema_for(fn) for fn in TOOLS.values()]

# ---------------------------------------------------------------------------
# The loop
# ---------------------------------------------------------------------------

def run_agent(user_request: str, *, debug: bool = False) -> str:
    client = anthropic.Anthropic()
    messages: list[dict[str, Any]] = [{"role": "user", "content": user_request}]

    for iteration in range(1, MAX_ITERATIONS + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "max_tokens":
            return "error: the model's turn was truncated (max_tokens); raise max_tokens or shorten the context"
        tool_uses = [b for b in response.content if b.type == "tool_use"]
        if not tool_uses:
            # No tool call: the model decided it is done.
            return "".join(b.text for b in response.content if b.type == "text")

        results = []
        for tu in tool_uses:
            fn = TOOLS.get(tu.name)
            if fn is None:
                out = f"error: unknown tool {tu.name}"
            else:
                try:
                    out = fn(**tu.input)
                except Exception as e:  # last line of defence: still return text, never crash the loop
                    out = f"error: {type(e).__name__}: {e}"
            out = str(out)[:MAX_TOOL_RESULT_CHARS]
            if debug:
                print(f"[{iteration}] {tu.name}({json.dumps(tu.input)}) -> {out[:300]!r}")
            results.append({"type": "tool_result", "tool_use_id": tu.id, "content": out})
        messages.append({"role": "user", "content": results})

    return f"error: stopped after {MAX_ITERATIONS} iterations without a final answer"


if __name__ == "__main__":
    import sys
    print(run_agent(" ".join(sys.argv[1:]) or "<<example request>>", debug=True))
