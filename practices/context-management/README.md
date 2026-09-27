---
title: "Practice — context management: budget and triggers, reversible compaction, isolation rules, the long-context / cached-corpus / retrieval decision, and the metrics that prove it works"
type: practice
status: draft            # draft until principle 11 is confirmed against LIDR session 2
date: 2026-09-27
last-reviewed: 2026-09-27
tags: [context-engineering, compaction, prompt-caching, sub-agents, long-context, rag, evals]
kind: capability
applies-when: "multi_turn or retrieval"
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

## Adapt
- `context-budget-and-triggers.md`: fill the window and trigger for the model actually used; numbers rot — date them. A chat product and an agent loop get different recency windows.
- `compaction_skeleton.py`: set `<<TRIGGER_UTILISATION>>`, `<<KEEP_RECENT_TURNS>>`, `<<SUMMARY_MODEL>>`; implement `is_persisted()` for your tools (which results carry a path/URL/id); if a framework's middleware exists (LangChain summarization middleware, Strands context manager, Deep Agents), configure it with the same rules instead of copying the file — the rules are the deliverable.
- `context-store-decision.md`: answer the questions once per corpus; write the answer and the date into the spec.
- `context-metrics-and-evals.md`: wire the log lines into whatever tracing you have (Langfuse, LangSmith, OpenTelemetry GenAI attributes); the long-session eval needs real transcripts — collect ten from production first.
- Stack variants: Python shown; TypeScript is a direct port; the policy files are language-free.

## Verify
- The usage log shows, per call, input / output / cached tokens and context size; per session, cache hit rate. From the second turn on, `cache_read > 0`.
- A session that reaches the trigger compacts: the transcript shrinks, the system prompt is byte-identical before and after, the last `KEEP_RECENT_TURNS` turns are verbatim, and every compacted tool result still has a pointer that resolves.
- The long-session eval (`context-metrics-and-evals.md`) passes: turn N+1 answers correctly with the compacted history, at least 5/5 runs.
- No timestamp, user name, working directory or changing tool list appears before the `--- dynamic ---` line of the system prompt (`../llm-api-calls/system-prompt-template.md`).
- Every sub-agent's final message is self-contained (test: hand it to a fresh model with no history and ask for the conclusion).
- The corpus decision is written in the spec with the date and the reason.
- One trace per week has been read and the failure mode named, or "none seen".

## Sources
`sources/2026-09-27-s02-context-caching-digest.md` §3.1–3.6 and impact table §6; primary texts listed in `principles/11-runtime-context-management.md` §6. Vendor docs to re-check before promoting to `current`: Anthropic prompt caching and compaction docs; OpenAI prompt caching guide; Gemini context caching.

## Change log
- 2026-09-27 — created from the session-2 market scan (draft).
