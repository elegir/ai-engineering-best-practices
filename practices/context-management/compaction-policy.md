# Compaction policy — shrink the history without losing what matters

Copy into `<repo>/docs/context-policy.md` §compaction and reference it from the feature spec. Implementation: `compaction_skeleton.py` (or your framework's middleware configured with these rules). Principle: `../../principles/11-runtime-context-management.md` §3.2. Sources: Manus (LangChain webinar, 2025-10), LangChain summarization middleware (2025-11), AWS Strands (2026-09), Arize (AI Engineer, 2026-05), Hugging Face (2026-08) — `../../sources/2026-09-27-s02-context-caching-digest.md` §3.2, §5.

## The ladder — cheapest and safest first

**Step 0 — Offload at the source.** Any tool result whose content is persisted somewhere addressable (file path, URL, query, record id) enters the transcript as a *preview + pointer*, never as the full payload. Cap: <<2,500>> tokens → store, keep a <<500>>-token preview. This is not compaction; it prevents the need for it. Tool authors: return the identifier with, or instead of, the payload (`../agent-patterns/tool-definition-template.md`).

**Step 1 — Reversible compaction.** When utilisation reaches the trigger (<<60–85 %>>), walk the **oldest ~50 %** of tool results and strip the payload of every one that is persisted, leaving the pointer ("`read_file(path=a.py)` → `[content offloaded; re-read a.py if needed]`"). Nothing is lost: "no information is truly lost, it's just externalized" (Manus). Also **deduplicate** repeated identical tool results (Arize). Leave the recent turns and the system prompt untouched.

**Step 2 — Schema-constrained summary.** Only when step 1 does not free enough. Rules, each one backed by a production failure when ignored:
- Summarise the **oldest half**; keep the **last <<N>> turns verbatim** — the model copies the format of recent tool calls, and if those are all compacted it starts emitting malformed calls.
- Summarise **from the full record**, never from already-compacted history; splice the verbatim recent turns **after** the summary.
- Prompt the summary as a **schema**, not "please summarise": `goal`, `constraints_and_user_preferences`, `files_or_records_touched` (with pointers), `decisions_taken`, `current_state / where_I_left_off`, `open_questions`, `errors_seen_and_resolved`. Structured output is stable and can be iterated; free-form was "too inconsistent — no control over what got dropped" (Arize).
- Add a **preserve list** per feature (the requirement that must survive every compaction, e.g. "the customer's order id and stated deadline").
- Run it on a **cheaper model**; the summary is extraction, not reasoning.
- **Never reset or rewrite the system prompt.**
- Prefix the summary with a fixed marker (`[Previous conversation summary]`) so traces and evals can find it.

**Option B — Head + tail with retrievable middle (Arize).** If summaries still drop what matters in your domain: keep the first <<K>> and last <<K>> tokens/turns verbatim, move the middle to a store, give the agent a `recall(topic)` tool over it, deduplicate repeated results. This held in production for months where summarisation had not.

## What compaction does to the cache

Compaction rewrites history, so the provider's prefix cache restarts from the compaction point. Expected, not a bug — but it means: compact **rarely and decisively** (one big compaction at the trigger beats many small ones), and never compact the static prefix (system prompt, tool definitions, cached corpus).

## Never

- Summarise the whole history including the system prompt with the main model and a one-line prompt.
- Drop a tool result that was never persisted anywhere (lossy by accident).
- Compact the recent turns.
- Change the tool list or the system prompt as part of "cleaning up".
- Continue a session whose trajectory is a chain of failed retries: compact into a verified note and **start a new session** instead.

## Isolation is the other half

When one sub-task produces disproportionate tokens (log parsing, a search over hundreds of records, a long document read), do not compact it in place — run it in a **sub-agent with its own window** that returns a self-contained digest (`context-metrics-and-evals.md` §isolation rules; `../agent-patterns/patterns-catalogue.md`).
