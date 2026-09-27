"""compaction_skeleton.py — shrink an agent's message history without losing what matters.

Copy to <repo>/src/<package>/context.py. Replace <<TRIGGER_UTILISATION>>, <<KEEP_RECENT_TURNS>>,
<<SUMMARY_MODEL>> and implement `is_persisted()` for your tools.
Policy: practices/context-management/compaction-policy.md. Principle: principles/11-runtime-context-management.md §3.2.

The ladder, cheapest first:
  step 1  reversible compaction — strip the payload of OLD tool results that are persisted elsewhere; keep the pointer
  step 2  schema-constrained summary of the OLD half on a cheap model; recent turns stay verbatim; system prompt untouched
Call `maybe_compact(items, usage)` before every model call. Works on the item/message list you own
(practices/llm-api-calls/llm_call_skeleton.py); the system prompt is NOT in `items`, so it cannot be touched here.
"""
from __future__ import annotations

import json
from typing import Any

TRIGGER_UTILISATION = <<TRIGGER_UTILISATION>>   # e.g. 0.75 — compaction is a quality decision, not a capacity one
KEEP_RECENT_TURNS = <<KEEP_RECENT_TURNS>>       # e.g. 6 — the model imitates the format of recent tool calls; keep them verbatim
SUMMARY_MODEL = "<<SUMMARY_MODEL>>"             # cheap tier; the summary is extraction, not reasoning
CONTEXT_WINDOW = <<CONTEXT_WINDOW>>             # tokens, per the model's docs; dated in docs/context-policy.md
SUMMARY_MARKER = "[Previous conversation summary]"

# Fields a summary must fill. Free-form "please summarise" is what failed in production (Arize).
SUMMARY_SCHEMA = {
    "type": "object",
    "properties": {
        "goal": {"type": "string"},
        "constraints_and_user_preferences": {"type": "array", "items": {"type": "string"}},
        "files_or_records_touched": {"type": "array", "items": {"type": "string"},
                                     "description": "paths / ids / URLs, so anything can be re-read"},
        "decisions_taken": {"type": "array", "items": {"type": "string"}},
        "current_state": {"type": "string", "description": "where I left off"},
        "open_questions": {"type": "array", "items": {"type": "string"}},
        "errors_seen_and_resolved": {"type": "array", "items": {"type": "string"}},
        "must_preserve": {"type": "array", "items": {"type": "string"},
                          "description": "<<PRESERVE LIST for this feature, e.g. order id, deadline>>"},
    },
    "required": ["goal", "current_state", "files_or_records_touched", "must_preserve"],
}


def is_persisted(tool_name: str, tool_input: dict[str, Any], result_text: str) -> str | None:
    """Return the pointer that lets the result be re-read later, or None if the result exists nowhere else.
    <<IMPLEMENT PER TOOL>>: a read_file result → its path; a fetch → its URL; a search → its query;
    a DB read → the record id. A tool whose result is NOT persisted anywhere must never be compacted (lossy)."""
    if tool_name in ("read_file", "list_dir") and "path" in tool_input:
        return f"path={tool_input['path']}"
    if tool_name == "fetch_url" and "url" in tool_input:
        return f"url={tool_input['url']}"
    return None


def utilisation(usage: dict[str, int]) -> float:
    """Fraction of the window used by the last call (input tokens incl. cached), from the usage log."""
    return (usage.get("input", 0) + usage.get("cache_read", 0)) / CONTEXT_WINDOW


def _split(items: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Old part (compactable) vs recent turns (kept verbatim). A 'turn' = one user or assistant item."""
    cut = max(0, len(items) - KEEP_RECENT_TURNS)
    return items[:cut], items[cut:]


def reversible_compaction(old: list[dict[str, Any]], tool_calls_by_id: dict[str, tuple[str, dict]]) -> list[dict[str, Any]]:
    """Step 1: strip payloads of persisted tool results in the OLD part; keep a pointer. Deduplicate identical results."""
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for item in old:
        content = item.get("content")
        if not isinstance(content, list):
            out.append(item)
            continue
        new_blocks = []
        for b in content:
            if b.get("type") != "tool_result":
                new_blocks.append(b)
                continue
            text = b["content"] if isinstance(b["content"], str) else json.dumps(b["content"])
            name, tool_input = tool_calls_by_id.get(b["tool_use_id"], ("", {}))
            key = f"{name}:{json.dumps(tool_input, sort_keys=True)}"
            pointer = is_persisted(name, tool_input, text)
            if key in seen:
                new_blocks.append({**b, "content": "[duplicate result removed; identical to an earlier call]"})
            elif pointer:
                new_blocks.append({**b, "content": f"[content offloaded to save context; re-read with {name}({pointer}) if needed]"})
            else:
                new_blocks.append(b)  # not persisted anywhere → keep (lossy otherwise)
            seen.add(key)
        out.append({**item, "content": new_blocks})
    return out


def structured_summary(old_full_record: list[dict[str, Any]], call) -> dict[str, Any]:
    """Step 2: summarise the OLD half — from the FULL record, not the compacted one — into SUMMARY_SCHEMA.
    `call` is your client (practices/llm-api-calls/llm_call_skeleton.py: call(system, items, tools, model=...))."""
    system = ("You compress an agent's conversation history so the agent can continue the task. "
              "Fill every field of the schema from the transcript. Keep every id, path, URL and number verbatim. "
              "Do not add anything that is not in the transcript.")
    items = [{"role": "user", "content": "Transcript:\n" + json.dumps(old_full_record)[:400_000] +
              "\n\nReturn ONLY a JSON object matching this schema:\n" + json.dumps(SUMMARY_SCHEMA)}]
    res = call(system, items, model=SUMMARY_MODEL)
    if res.error:
        raise RuntimeError(f"summary failed: {res.error}")  # caller decides: retry or skip compaction this turn
    return _first_json_object(res.text)


def _first_json_object(text: str) -> dict[str, Any]:
    """Extract the first balanced {...} object from text that may wrap it in prose or ```json fences.
    Prefer the provider's structured-output / tool-call mode when available; this is the fallback."""
    text = text.replace("```json", "```").replace("```", "")
    start = text.find("{")
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        c = text[i]
        if in_str:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == '"': in_str = False
            continue
        if c == '"': in_str = True
        elif c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise ValueError("no JSON object in summary output")


def _unpersisted_blocks(old: list[dict[str, Any]], tool_calls_by_id: dict[str, tuple[str, dict]]) -> list[dict[str, Any]]:
    """Tool results that exist nowhere else. The policy says these are never dropped, so step 2 carries them over verbatim."""
    keep: list[dict[str, Any]] = []
    for item in old:
        content = item.get("content")
        if not isinstance(content, list):
            continue
        for b in content:
            if b.get("type") != "tool_result":
                continue
            name, tool_input = tool_calls_by_id.get(b["tool_use_id"], ("", {}))
            text = b["content"] if isinstance(b["content"], str) else json.dumps(b["content"])
            if is_persisted(name, tool_input, text) is None:
                keep.append({"tool": name, "input": tool_input, "result": text})
    return keep


def maybe_compact(items: list[dict[str, Any]], usage: dict[str, int], call,
                  tool_calls_by_id: dict[str, tuple[str, dict]]) -> list[dict[str, Any]]:
    """Run before each model call. Returns the (possibly) compacted item list. System prompt is not in `items`."""
    if utilisation(usage) < TRIGGER_UTILISATION:
        return items
    old, recent = _split(items)
    if not old:
        return items
    # step 1: reversible
    compacted_old = reversible_compaction(old, tool_calls_by_id)
    est = len(json.dumps(compacted_old)) // 4  # rough tokens
    if est < CONTEXT_WINDOW * 0.35:            # freed enough → stop here; nothing lost
        return compacted_old + recent
    # step 2: lossy but structured; summarise from the FULL old record, then splice recent turns AFTER it
    summary = structured_summary(old, call)
    # Results that were never persisted anywhere are NOT summarised away (policy: never lossy by accident).
    unpersisted = _unpersisted_blocks(old, tool_calls_by_id)
    summary_text = f"{SUMMARY_MARKER}\n{json.dumps(summary, indent=1)}"
    if unpersisted:
        summary_text += "\n\n[Tool results kept verbatim because they exist nowhere else]\n" + json.dumps(unpersisted, indent=1)
    summary_item = {"role": "user", "content": summary_text}
    ack = {"role": "assistant", "content": "Understood. I will continue from this state."}
    return [summary_item, ack] + recent
