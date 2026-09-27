---
title: "Runtime context management — the window is a budget, not a container: offload, reduce, retrieve, isolate and cache, and when to use long context, a cached corpus or retrieval"
type: principle
status: draft              # draft until LIDR session 2 (2026-10-22) confirms or contradicts
date: 2026-09-27
last-reviewed: 2026-09-27
tags: [context-engineering, context-window, compaction, prompt-caching, kv-cache, cag, long-context, rag, sub-agents, s2]
sources:
  - sources/2026-09-27-s02-context-caching-digest.md
  - sources/2026-09-27-market-scan-s02-context-caching.md
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - https://arxiv.org/abs/2412.15605
  - https://www.trychroma.com/research/context-rot
supersedes: null
superseded-by: null
---

# Runtime context management

## 1. The question this answers

When a product keeps a conversation or an agent loop going across many model calls, or answers over a body of documents, what goes into the context window on each call, what is kept out, how is the history shrunk without losing what matters, how is the provider's cache kept warm, and when is it right to put a whole corpus in the window instead of retrieving from it?

## 2. Short answer

Treat the context window as **working memory with a budget**, not as a container to fill: quality falls long before the advertised limit ("context rot"), so plan to stay well below it and to start fresh when the task changes. Manage the window with five operations, in this order of cheapness. **Offload**: anything a tool has already persisted (a file, a URL, a query) leaves the transcript and stays as a pointer. **Reduce**: first *reversible compaction* (drop payloads whose pointer survives), then, only when that is not enough, *schema-constrained summarisation* of the oldest half of the history, keeping the recent turns verbatim, summarising from the full record, using a cheap model, and never touching the system prompt. **Retrieve**: bring back only what this step needs; for code and documentation a curated manifest with good descriptions plus grep beats a vector index more often than not. **Isolate**: give noisy sub-tasks their own window in a sub-agent that returns a *self-contained* digest; fan out only read-only gathering and converge for anything that must cohere. **Cache**: keep the request's prefix static and append-only so the provider's KV cache hits — that cuts cost from quadratic to linear over a session and does nothing for quality. Choose the corpus strategy by shape: a bounded, stable corpus needing whole-document reasoning goes in the window and is cached (this is what the literature calls CAG); an unbounded or fast-changing corpus is retrieved. Instrument all of it: context size per call, cache hit rate per request and per session, and a long-session eval that loads N turns and tests turn N+1.

## 3. Long explanation

### 3.1 The window is a budget

Three independent kinds of evidence say the same thing (`sources/2026-09-27-s02-context-caching-digest.md` §3.1). The measurements: Chroma's *Context Rot* (18 models, 2025-07) and the needle-in-a-haystack studies Anthropic's engineering post cites show accuracy falling as input grows, non-uniformly, on simple tasks; *Lost in the Middle* (Liu et al., 2023) gives the shape — the edges are recalled, the middle is lost. The practitioners: Manus compacts at roughly 128–200k tokens on models sold with a 1M window; LangChain's middleware triggers at 80 % of the model's window by default; AWS demonstrates 85 %; Dex Horthy's rule is blunt — "the less context window you use, the better outcomes you'll get, always". And the mechanism: the weights are a vague recollection, the window is the working memory (`10-llm-api-fundamentals.md` §3.1), and working memory that is full of stale material is worse than working memory that is short.

Two more budgets share the same window. The **instruction budget**: directives accumulate — including ones the user has since reversed — and each stale instruction competes for attention with the current one; when a requirement changes mid-session, replace or compact, do not append (Horthy). The **trajectory**: the model is autoregressive, so a history of failed attempts and "you're absolutely right" corrections predicts more of the same; the fix is a fresh window carrying only a verified summary, not one more prompt in the same session. The coding-agent form of the rule (Claude, 2026-05): compact to continue the same feature, clear to start another, because "you don't want the previous conversation to present bias in anything new".

Four named failure modes to look for in a trace (Drew Breunig, via Google Cloud and LangChain): **poisoning** (a hallucination lodged in history is reused as fact), **distraction** (the model leans on the long history instead of planning afresh), **confusion** (irrelevant detail steers the answer), **clash** (two sources disagree and the wrong one wins). Naming them is what makes the fix findable: poisoning → prune or restart; distraction → compact; confusion → select less; clash → dedupe and date the sources.

### 3.2 The five operations

The taxonomy is Lance Martin's (offload / reduce / retrieve / isolate / cache; his earlier write / select / compress / isolate is the same set and is what Google Cloud and LangChain teach). Each operation, with the rules the sources agree on:

**Offload.** Every tool result whose content is already persisted somewhere addressable can leave the transcript and be re-read on demand — "no information is truly lost, it's just externalized" (Manus). A file system, real or a "virtual" one backed by a database, is therefore a first-class agent capability (LangChain Deep Agents; Manus; AWS shows the concrete shape: results above ~2,500 tokens go to storage with a 500-token preview and a retrieval tool). Design consequence for tool authors: **return an identifier with, or instead of, the payload**; that is what makes later compaction lossless. Notes and plans belong outside the window too (a scratchpad file the agent re-reads), which is the runtime version of `practices/session-state/`.

**Reduce.** Distinguish *compaction* (reversible: strip the `content` field, keep the `path`) from *summarisation* (lossy), and escalate to the second only when the first stops freeing enough space (Manus). Rules for summarising that three vendors state independently and one vendor's failure confirms: compact or summarise the **oldest ~50 %** and keep the recent turns **verbatim** — the model imitates the format of the recent tool calls, and if they are all compacted it starts emitting malformed calls; summarise **from the full record**, never from already-compacted history; splice the last N raw exchanges *after* the summary; prompt the summary as a **schema** (goal, files touched, decisions taken, where I left off, open questions) rather than "please summarise", because structured output is stable and can be iterated; run the summariser on a **cheaper model**; **never reset the system prompt**. The dissent that fixes the rule is Arize's: an unconstrained summariser was "too inconsistent — no control over what got dropped", head-only truncation broke follow-ups, and what has held in production is head + tail preserved, the middle stored and retrievable, repeated tool results deduplicated. Read together: free-form summarisation is not production-viable; reversible compaction is always safe; summarisation is acceptable when schema-constrained, recency-exempt and fed the full record. Compaction rewrites history and therefore resets the provider cache; that is expected, not a bug.

**Retrieve.** "Selection, not hoarding" (Google Cloud). Bring back, per step, only what the step needs. Two findings change the default for code and documentation: Lance Martin's own test on ~3M tokens of docs — a curated `llms.txt` (file list with LLM-written one-line descriptions) plus a plain fetch tool beat both a vector store and context-stuffing when driven by a coding agent, and *description quality* was the dominant variable; and the leading coding agents (Claude Code, Cline, as reported) do no indexing at all, only agentic grep/glob, while Manus's answer is "no index for a task, an index for an enterprise knowledge base". Instructions are retrieved the same way: split a system prompt that covers many workflows into skills loaded on demand (progressive disclosure of *instructions*, the twin of progressive disclosure of tools in `21-agent-design-and-tools.md` §3.4). The full retrieval discipline (chunking, reranking, metadata at ingestion) belongs to the RAG sessions; `practices/context-management/context-store-decision.md` gives the decision now.

**Isolate.** A sub-agent with its own window does the noisy work and returns a digest; the orchestrator's context stays light and reusable (AWS, Arize, Claude). Three rules the s12 principle did not have. (1) **Only the final message crosses the boundary** — a sub-agent told to "refer to the work above" leaves the orchestrator blind; require a self-contained final message (Harrison Chase). (2) Two patterns: *communicate* (a short brief in, a structured result out — Claude Code's Task tool) and *share memory* (the sub-agent inherits the whole history); the second forfeits the cache entirely because the sub-agent's prefix differs from the parent's — "you have to pay the full price" (Manus). Default to *communicate*. (3) Fan out only **read-only, independent gathering**; do every step that must cohere — the final report, code that must integrate — in one agent. This reconciles Cognition's "don't build multi-agent" with Anthropic's multi-agent researcher, and Martin's own bug (sections written inside sub-agents made a disjoint report) is the confirmation. Manus adds: no role-based agents mimicking an org chart; an executor, a planner and a memory agent, because every extra agent multiplies communication.

**Cache.** §3.3.

### 3.3 The cache and the economics

Prompt caching is **prefix caching of the KV tensors**: the provider matches the new request against the stored one token by token from the start and recomputes from the first difference (IBM; Hugging Face). The rule is therefore *static first, dynamic last, append-only* (`10-llm-api-fundamentals.md` §3.4), and the list of what breaks it is short and worth memorising: a timestamp, a current directory or a user name at the top of the system prompt; a tool list that changes between turns; any edit to an earlier message; and compaction, which legitimately restarts it. Manus draws the architectural conclusion: never load tools dynamically mid-session (it invalidates the cache *and* leaves the model remembering tools that no longer exist); keep a fixed set of ~10–20 atomic functions ("try not to include more than 30") and grow capability through a sandboxed shell with `--help` discovery and through code, so the schema never changes.

Why it matters more for agents than for chat: the transcript is re-sent on every turn, so a session's cost is 50k + 51k + 54k + 55k… tokens — quadratic without caching, roughly linear with it — and cache reads cost about a tenth of fresh input on the expensive providers (Hugging Face; IBM; Anthropic's docs price writes at 1.25×/2× and reads at 0.1×). At an input-heavy, output-light ratio, Manus reports that hosted frontier models can come out *cheaper* than open-weight ones once hit rate is counted, and that distributed KV-cache infrastructure is hard to replicate outside the large providers. So **choose a model on cached-input price and cache infrastructure, not sticker price** (row 10 of `practices/llm-api-calls/provider-selection-checklist.md`).

What caching does *not* do: improve quality. Context rot applies whether or not the tokens are cached (Martin, with Anthropic's confirmation); "prompt caching isn't really a context engineering technique because we're not changing what goes into the context window" (AWS). A high hit rate is not a licence to keep stuffing. Operational details: a minimum cacheable prefix of about 1,024 tokens; TTLs from five minutes to an hour depending on provider and setting, so a cache expires over a lunch break and is rewritten at full price; automatic prefix caching on some APIs, explicit breakpoints or cache objects on others — the speakers were unsure of the current state live, so check the provider's docs, not the talk. Measure hit rate per request and per session; a multi-turn feature with zero cached tokens has its prompt in the wrong order.

### 3.4 Long context, cached corpus (CAG) or retrieval

**CAG** (Chan et al., *Don't Do RAG*, 2024-12) is: prepare a bounded corpus that fits the window → pre-compute its KV cache once → persist it → answer every query by loading the cache and appending the question. The paper reports large speed-ups over re-processing; the limits are that the corpus must fit and must be stable, since any change recomputes everything. **Prompt caching is CAG as a service** (IBM): the provider manages the KV cache for a long, stable prefix, which is why the research idea became usable without infrastructure. Practitioners do not use the acronym; they say prompt caching.

**The decision** (IBM's two lists, agreed by Manus and Airbyte). For putting the corpus in the window: it collapses the infrastructure (no chunking, embeddings, vector store, reranker, sync); there is no *retrieval lottery* — no silent failure where the answer existed and retrieval never returned it; and it solves the **whole-book problem**: "which security requirements were omitted from the release?" needs both documents in full, and retrieval returns snippets of each but can never retrieve the gap between them. For retrieval: the re-reading tax (a 250k-token manual processed on every query, offset by caching only when the data is stable); the haystack (attention dilutes; top-k hands over the needles without the hay); and the unbounded set (enterprise data in terabytes never fits). Rule: **bounded, stable corpus with global reasoning → in the window, cached; unbounded or fast-changing → retrieve; code and docs for an agent → agentic search first, an index when scale demands it.** When an upstream API cannot filter the way the question needs, the agent will page the whole set through its window — pre-filter or pre-index outside the model (Airbyte's demo, vendor numbers). "RAG is not dead, just the way we're doing it" (Tricot): the depth — metadata at ingestion, reranking, document parsing — is the RAG sessions' business.

### 3.5 The harness owns the policy

Compaction triggers and strategy are decided by the harness author today; a few labs let the model decide when to compact, and the direction is toward less scaffolding as models improve — "build less and understand more" (Manus, whose harness has been rebuilt five times since March 2025; the same lesson Notion gave the s12 digest). Two things the harness must therefore provide from day one. **Traces**: "you don't actually know what the context at step 14 will be, because there's 13 steps before that that could pull arbitrary things in" (Chase); bugs invisible in a five-turn dev test appear at turn 10–20 in production and are obvious in a full trace (Ebbelaar). **Long-session evals**: load ten turns, test the eleventh (Arize) — the reproducible form of a context-management regression. And a working method for people as well as agents: research → plan → implement, each phase compacted into a small, human-verifiable artifact and the next phase started in a fresh window (Horthy's "intentional, frequent compaction"). Those per-task artifacts are throw-away; the durable documents are the conventions and standards of `01-context-engineering.md`.

## 4. How to apply it in a repo

1. Confirm the facts `multi_turn` and/or `retrieval` (`practices/facts.md`); if either holds, `practices/context-management/` applies.
2. Log, per call, input / output / cached tokens and the context size; add a per-session cache-hit rate. Without these numbers nothing below can be verified (`practices/llm-api-calls/llm_call_skeleton.py` already logs them).
3. Fill `practices/context-management/context-budget-and-triggers.md`: the model's window, the compaction trigger (60–85 % or the vendor's guidance), the recency window kept verbatim, the truncation policy for tool results.
4. Make tool results addressable: every tool that returns more than a screenful returns an id/path/URL; copy the rule into each tool's docstring (`practices/agent-patterns/tool-definition-template.md`).
5. Implement compaction from `compaction-policy.md` and `compaction_skeleton.py`: reversible compaction first, schema-constrained summary second, system prompt untouched, recent turns verbatim.
6. Keep the prefix static: no timestamps, user names or changing tool lists at the top; a fixed tool set; dynamic content at the end. Verify with the cache-hit log.
7. For sub-agents, use the *communicate* pattern and require a self-contained final message; fan out only read-only work.
8. Decide the corpus strategy once with `context-store-decision.md` and write the answer into the feature spec.
9. Add a long-session eval (N turns in, test N+1) to the feature's eval set; run it in CI.
10. Read one full trace per week; name the failure mode you see (poisoning, distraction, confusion, clash) and fix that, not the prompt.

## 5. Anti-patterns

- Treating a 1M-token window as a reason to skip context management; discovering at turn 15 that answers have gone vague.
- Summarising the whole history with "please summarise the conversation" on the main model, including the system prompt, from already-compacted history.
- Dropping tool results that were never persisted anywhere (lossy by accident) — or keeping full log dumps in the transcript because "the model might need them".
- A timestamp, a working directory or a per-user greeting at the top of the system prompt; a tool list that changes per turn.
- Sharing the full history with every sub-agent, or writing coherent output (a report, integrated code) in parallel sub-agents.
- Building a vector pipeline for a bounded, stable corpus that fits the window, or stuffing an unbounded, changing one into it.
- Appending a new instruction when the user reverses an old one, and continuing a session whose trajectory is a chain of failed retries.
- Reading no traces and running no long-session evals, then tuning the prompt when the problem is the context.

## 6. Evidence & sources

- Digest with the impact table — `sources/2026-09-27-s02-context-caching-digest.md`; scan log — `sources/2026-09-27-market-scan-s02-context-caching.md`; transcripts in `sources/raw/2026-09-27-market-scan-s02-context-caching/`.
- Taxonomy and practitioner rules: Lance Martin, *Context Engineering for Agents* (Latent Space, 2025-09; LangChain webinar with Manus, 2025-10); Harrison Chase (Sequoia, 2026-01); Dex Horthy (Pragmatic Engineer, 2026-07); Sally-Ann DeLucia, Arize (AI Engineer, 2026-05); AWS Developers (2026-09); Dave Ebbelaar (2025-12) restating Anthropic's post.
- Caching and economics: Hugging Face (2026-08); IBM *What is prompt caching?* (2026-02); Manus (2025-10); Anthropic, OpenAI and Gemini caching docs (written canon).
- CAG and long context vs RAG: Chan et al. arXiv 2412.15605; IBM *CAG vs long context* (2026-05) and *Is RAG still needed?* (2026-03); Michel Tricot, Airbyte (Chain of Thought, 2026-03); Jerry Liu, LlamaIndex (AI Engineer, 2026-09).
- Degradation evidence: Chroma *Context Rot* (2025-07); Liu et al. *Lost in the Middle* (2023); Anthropic *Effective context engineering for AI agents* (2025-09-29).
- Vocabulary: Google Cloud Tech (2026-07); Claude *Context management in Claude Code* (2026-05); LangChain summarization middleware (2025-11).

## 7. Change log

- 2026-09-27 — created from `sources/2026-09-27-s02-context-caching-digest.md` (market scan for LIDR session 2). Status `draft` until the session on 2026-10-22.
