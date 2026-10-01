---
title: "Practice — context management: budget and triggers, reversible compaction, isolation rules, the long-context / cached-corpus / retrieval decision, and the metrics that prove it works"
type: practice
status: draft            # draft until principle 11 is confirmed against LIDR session 2
date: 2026-09-27
last-reviewed: 2026-10-01
tags: [context-engineering, compaction, prompt-caching, sub-agents, long-context, rag, evals]
kind: capability
applies-when: "multi_turn or retrieval"
when: first-user   # day-0 | first-user | at-scale — when in a product's life this practice is installed (decision 0004 §5)
reference-status: untested   # untested | field-tested | reference (decision 0005 §3)
principle: principles/11-runtime-context-management.md
sources:
  - sources/2026-09-27-s02-context-caching-digest.md
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - https://docs.claude.com/en/docs/build-with-claude/prompt-caching
supersedes: null
superseded-by: null
---

# Context management

## Solves
The product keeps a conversation or an agent loop across many model calls, or answers over a body of documents, and one of these symptoms appears: answers get vague or wrong after ten or twenty turns and nobody can say why; the transcript is re-sent whole on every turn and the bill grows faster than usage; the history is "summarised" by an unconstrained prompt and follow-ups break; tool results are either dumped in full into the context or dropped for good; sub-agents get the whole history (no cache) or return "see above" (orchestrator blind); a vector pipeline was built for a corpus that fits in the window, or a changing corpus is stuffed into it; there is no trace of what the model saw at step N and no test that loads N turns and checks turn N+1.

## Applies when
- The fact `multi_turn` holds (`../facts.md`): history is passed back into the model — a chat feature, an assistant with memory of the session, any agent loop.
- Or the fact `retrieval` holds: the product answers over documents or data fetched at query time (this folder gives the *decision* between long context, cached corpus and retrieval; the retrieval pipeline itself is the RAG practice, pending).

## Does not apply when
- Every call is single-shot with a short prompt and no history (a classifier, an extractor). Then only `../llm-api-calls/` applies (its `context-budget.md` covers prefix ordering and caching for one call).
- The only model in the picture is the coding agent working on the repo — `../token-savings/` and `../session-state/` are the coding-agent versions of the same ideas.
- The question is *which* retrieval pipeline (chunking, embeddings, reranking, metadata) — RAG practice, sessions 9–11 (pending).

## Files in this folder
| File | Copy to | Purpose |
|---|---|---|
| `context-budget-and-triggers.md` | `<repo>/docs/context-policy.md` | The numbers per feature: window, compaction trigger, recency window, tool-result cap, what stays static; the seven-part context stack as a checklist |
| `compaction-policy.md` | `<repo>/docs/context-policy.md` §compaction (and the feature spec) | Reversible compaction → schema-constrained summary → (option B) head+tail with retrievable middle; the rules that make each safe |
| `compaction_skeleton.py` | `<repo>/src/<package>/context.py` | ~90 lines: reversible compaction of persisted tool results, utilisation trigger, structured summary on a cheap model, recent turns kept verbatim, system prompt untouched |
| `context-failure-modes.md` | read; keep next to the trace viewer | Poisoning / distraction / confusion / clash / stale instructions / bad trajectory: symptom in a trace, cause, fix; the contested "leave errors in vs prune" |
| `context-store-decision.md` | `<repo>/docs/architecture.md` §knowledge, or the feature spec | Long context vs cached corpus (CAG) vs retrieval vs agentic search: the decision table and the questions that decide it |
| `context-metrics-and-evals.md` | `<repo>/docs/context-policy.md` §metrics; `<repo>/evals/` | What to log per call and per session; the long-session eval (N turns in, test N+1); the isolation rules for sub-agents |

## Reference implementation

`compaction_skeleton.py` — the compaction policy with its invariants (recent turns verbatim, pointers for tool results, prompt untouched). Python idioms not in the contract: the dataclass transcript and the JSON summary format; a framework's memory module satisfies the contract if assertion 2 holds against it.

## Stack-sensitive points

- Where the transcript lives decides everything: a long-lived process keeps it in memory; a request-scoped runtime (PHP-FPM, serverless) must load it from a store on every call, so compaction runs as a step of the request or as a job, never "in the background".
- Prompt caching is a vendor feature with different switches per SDK (`cache_control` blocks for Anthropic; automatic prefix caching elsewhere) — the assertion is about cached tokens being read, not about which flag does it.
- Token counting: Python/TS SDKs expose a counter; in PHP estimate (characters ÷ 4) and keep the trigger conservative.

## Adapt
- `context-budget-and-triggers.md`: fill the window and trigger for the model actually used; numbers rot — date them. A chat product and an agent loop get different recency windows.
- `compaction_skeleton.py`: set `<<TRIGGER_UTILISATION>>`, `<<KEEP_RECENT_TURNS>>`, `<<SUMMARY_MODEL>>`; implement `is_persisted()` for your tools (which results carry a path/URL/id); if a framework's middleware exists (LangChain summarization middleware, Strands context manager, Deep Agents), configure it with the same rules instead of copying the file — the rules are the deliverable.
- `context-store-decision.md`: answer the questions once per corpus; write the answer and the date into the spec.
- `context-metrics-and-evals.md`: wire the log lines into whatever tracing you have (Langfuse, LangSmith, OpenTelemetry GenAI attributes); the long-session eval needs real transcripts — collect ten from production first.
- Stacks: Python shown; the policy files are language-free; TypeScript is not a promised stack (decision 0005 §4) — implement from the contract until a field-tested variant exists.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

1. The usage log records, per model call, input, output and cached tokens plus the context size, and per session the cache hit rate; from the second turn of a conversation on, once the stable prefix exceeds the vendor's minimum cacheable length (about 1,024 tokens), cached tokens read is above zero — observer: script — negative: a later turn with a long stable prefix and zero cached tokens (the static/dynamic order is wrong)
2. When a session reaches the compaction trigger it compacts: the transcript shrinks, the system prompt is byte-identical before and after, the last `KEEP_RECENT_TURNS` turns are verbatim, and every compacted tool result keeps a pointer that resolves — observer: script — negative: a changed system prompt, a lost recent turn, or a pointer to nothing
3. The long-session eval in `context-metrics-and-evals.md` passes: turn N+1 is answered correctly from the compacted history in at least five runs out of five — observer: script — negative: one failed run (the mean hides it)
4. Nothing that changes per request (timestamp, user name, working directory, tool list) appears before the dynamic marker of the system prompt — observer: script — negative: a diff of two system prompts shows a difference above the marker
5. Every sub-agent's final message is self-contained: handed to a fresh model with no history, the conclusion is recoverable — observer: agent — negative: a sub-agent that answers "see above" or refers to context the parent never sent
6. The corpus decision (stuff the window, retrieve, or hybrid) is written in the feature spec with the date and the reason, per `context-store-decision.md` — observer: Martin — negative: a vector pipeline for a corpus that fits, or a corpus that changes stuffed into the window, with no written reason
7. (Ongoing — not required for field-tested.) One trace per week has been read and the failure mode named (or "none seen") in the practice's log — observer: Martin — negative: a month with no trace read

**Example commands (Python):** `python3 compaction_skeleton.py --demo`; the eval runner in `context-metrics-and-evals.md` §Runner.

## Sources
`sources/2026-09-27-s02-context-caching-digest.md` §3.1–3.6 and impact table §6; primary texts listed in `principles/11-runtime-context-management.md` §6. Vendor docs to re-check before promoting to `current`: Anthropic prompt caching and compaction docs; OpenAI prompt caching guide; Gemini context caching.

## Change log

- 2026-10-01 (s5) — `context-store-decision.md` gains a *memory substrate* row (file interface for the model; namespaced store with concurrency and audit behind the handler); `context-metrics-and-evals.md` §2 gains the cross-session case (a fact from session 1 recalled, a contradicted fact updated, in session N; five runs). Source `sources/2026-10-01-s05-context-memory-permissions-evals-digest.md` rows 30, 31.
- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-27 — created from the session-2 market scan (draft).
- 2026-09-30 (s3) — metrics file points at the OTel GenAI attribute names in `../llm-gateway/tracing-otel.md`.
