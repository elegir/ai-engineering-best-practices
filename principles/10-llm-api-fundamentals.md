---
title: "LLM API fundamentals — what a model call is, what the model can and cannot do, and how to prompt, budget and pick a provider from that"
type: principle
status: draft              # draft until LIDR session 1 (2026-10-15) confirms or contradicts
date: 2026-09-27
last-reviewed: 2026-09-30
tags: [llm-api, prompting, tokens, context-window, prompt-caching, reasoning-models, providers, hallucination, s1]
sources:
  - sources/2026-09-27-s01-llm-setup-digest.md
  - sources/2026-09-27-market-scan-s01-llm-setup.md
supersedes: null
superseded-by: null
---

# LLM API fundamentals

## 1. The question this answers

When a product calls a language model through an API, what is actually happening, what can the model be trusted to do and not do, and what follows for how we structure the call, write the prompt, budget tokens, choose a model tier and choose a provider?

## 2. Short answer

A model is a next-token predictor with a **fixed amount of computation per token**, whose knowledge is a **lossy compression** of its training text and whose only reliable memory is the **context window**. From that, five rules. (1) **Put what matters in the context**: retrieve it, paste it or return it from a tool; never rely on the model recalling a fact, number, identifier or date. (2) **Let the model spend tokens before answering** anything multi-step — the native thinking budget on a reasoning model, an explicit "show your work" on any other; never demand a bare final answer when reliability matters. (3) **Route what the model is structurally bad at to tools**: counting, exact string manipulation, arithmetic, fresh facts. (4) **Fluency is not evidence**: LLMs are plausibility engines, prompts have no guaranteed semantics, and one model checking another does not compound reliability because their failures are correlated — guarantees live in code, schemas, tool restrictions and deterministic checks, and reliability is measured as "right every time on this scenario", not as an aggregate pass rate. (5) **Treat the call as an engineered artifact**: the API is an agentic loop of typed items in and out; the prompt has a fixed structure, is written as a complete briefing for a competent stranger, is iterated against real inputs and edge cases, and is versioned like code; the stable part of the prompt goes first so that prompt caching works; provider choice is a checklist of API features and switching cost, kept cheap by a thin wrapper of your own.

## 3. Long explanation

### 3.1 What the model is, and what it cannot do

**Compression, not a database.** Pretraining compresses internet text roughly a hundredfold into weights (Karpathy, 2025-02). What comes back is a "gestalt": the model cannot tell from the inside whether it is recalling or confabulating, and its knowledge is one-directional (it knows who a celebrity's mother is and cannot answer the inverse — the "reversal curse"). Karpathy's formulation is the one to keep: *knowledge in the parameters is a vague recollection; knowledge in the tokens of the context window is the working memory.* He demonstrates it with a text the model has certainly seen — a chapter of *Pride and Prejudice* summarised from memory versus with the chapter pasted into the prompt — and the second is materially better. Every fact that matters therefore enters through the context (retrieval, an attached document, a tool result) or is verified by a tool. This is the mechanism behind `01-context-engineering.md`, which states the same rule for coding agents.

**Tokens, not characters.** The model sees byte-pair tokens (~100k-symbol vocabulary), never letters. That one fact predicts a class of failures — counting letters, exact substrings, precise spelling — that no prompt fixes and a code-execution tool fixes trivially (Karpathy's live demonstrations: "how many Rs in strawberry", counting dots in a string).

**Fixed compute per token — "models need tokens to think".** Each output token gets the same bounded computation. Asked for a moderately hard arithmetic answer "in one token", the model is wrong; asked to show intermediate steps, it is right, because the work is spread across tokens. This is why chain-of-thought works, and it is the reason for rule (2). On a **reasoning model** (trained with reinforcement learning on *verifiable* answers — maths, code with tests; the DeepSeek-R1 recipe) the thinking is native: use the vendor's thinking/effort parameter rather than hand-written "step 1, step 2" scaffolds, which Andrew Ng (2026-05) rightly calls 2022-era advice for those models. On a non-reasoning model, ask for the work before the answer. On either, do not require a bare final token for a multi-step problem. And reasoning pays where the answer can be *checked* (code, maths, schema-bound extraction) and is, in Dan Klein's words, "totally unnecessary" on open-ended tasks — so route by verifiability, not by prestige (`08-model-selection.md`). Closed vendors return only a *summary* of the chain of thought; do not build a feature on reading the model's literal reasoning.

**Swiss cheese.** Capability is not monotonic in difficulty: a model that solves graduate-level problems can insist that 9.11 > 9.9. Test the cases that matter; never extrapolate "easier, so surely fine".

**Plausibility, not truth.** "We have built not truth engines, not reliability engines, we've built plausibility engines" (Dan Klein, 2026-04). Three consequences. *Prompting has no semantics*: no wording guarantees a behaviour the way a function contract does, so where a guarantee is needed — money, irreversible actions, policy-bound answers — enforce it outside the model (schema validation, business rules, tool allow-lists, human approval). *Failures are correlated*: a second model checking the first does not multiply reliabilities as if independent ("80 % checking 80 %" lands near 82 %, not 96 %), and multi-turn conversations compound per-turn error; an LLM judge is a signal to combine with deterministic checks, never the only gate. *Measure consistency*: what ships is "for how many scenarios do I get it right every time, 100 times in a row" — run each test case N times and read the worst case. Detected hallucinations are the tip of an iceberg: "looks right and is right are not the same."

**Identity is prompted, not known.** "What model are you, what is your cutoff, what can you do" is itself a hallucination unless the answer is in the system prompt. Products that need it inject it.

### 3.2 The structure of a call

Both large vendors have converged on the same shape (OpenAI Responses API, Anthropic Messages API — `sources/2026-09-27-s01-llm-setup-digest.md` §3.2): the request carries **system instructions**, a list of **typed items** (user and assistant messages, tool calls, tool results, reasoning; Anthropic calls them content blocks) and **tool definitions**; the response is a list of typed output items, some of which are tool calls that *you* execute and append before calling again. "One string in, one string out" (Chat Completions) is legacy. The mental model of a call is therefore the agentic loop of `21-agent-design-and-tools.md` §3.2, even when the loop runs once.

**State.** Three options: own the item list and resend it (stateless, portable across vendors, satisfies zero-data-retention; what Anthropic requires); pass a `previous_response_id` and let the server chain (less to ship, vendor-bound); or a server-side conversation object. OpenAI returns **encrypted reasoning items** so a stateless client can still carry the model's reasoning across turns. The KB's default is to own the item list; adopt server-side state deliberately, per feature, with the lock-in written down.

**Keep the model's reasoning in the loop.** Passing reasoning items back into the next call raised tool-use accuracy and cut latency in OpenAI's own figures (+5 %, ~20 %; vendor numbers). The portable lesson is the same as "think like your agent": the model performs better when it sees its own plan, and you debug better when you can read it.

**Streaming is typed events** (item added, text delta, tool-call arguments delta, item done). Build clients on the event types, never on regex over text deltas.

**Hosted tools and remote MCP** (web search, file search, code execution, computer use; MCP servers attached to the request with `allowed_tools` and `require_approval`) are the vendor running tools server-side. They follow the KB's tool rules unchanged: "tools are prompts" (Anthropic), few and well-described per server, no stuffing of servers into one request (`21` §3.4–3.5; `practices/token-savings/mcp-audit.md`).

### 3.3 The prompt as an engineered artifact

**A fixed structure.** Anthropic's *Prompting 101* (2025-05) gives the order for a production prompt, each part a labelled section, XML tags where they help: task context and role → tone → background data and documents → detailed rules → examples → conversation history → the immediate request → thinking instructions → output format → prefilled start of the answer. Ordered steps beat paragraphs; the most important rules are repeated near the end; the output format is stated explicitly. Copyable version: `practices/llm-api-calls/system-prompt-template.md`. Ordering has a second purpose: the static parts come first so that prompt caching (§3.4) works.

**Clear communication, then iteration.** Anthropic's prompt-engineering roundtable (2024-09) reduces the craft to two things: write the way you would brief a *competent temp-agency worker who knows nothing about your company* — complete, explicit, with the actual paper or spec rather than a paraphrase, and without role-play the task does not need — and then **read the outputs** and iterate, against *real* inputs and *edge cases* (typos, empty input, off-topic), not against the ideal case. Give the model an out ("if none of these apply, say so"). Distinguish *illustrative* examples (show the shape) from *concrete* ones the model will copy too literally. An enterprise prompt must cover the *range* of inputs, not the median. Ask the model to critique the prompt or rewrite it, and use its words back — the same technique as `practices/prompt-library/trajectory-review.md`.

**Sycophancy is trained in.** Preference optimisation rewards agreement (Andrew Ng cites a reported ~10× ratio of agreement to disagreement). Neutral framing and factual criteria suppress it; "don't you think…?" invites it. Test it: A/B a leading and a neutral phrasing of the same question against your system prompt and look for drift.

**Versioned, not scattered.** OpenAI's dashboard prompt objects (id, version, variables) make the point structurally: a runtime prompt is an artifact with a version and a changelog, referenced from code by id, not a string literal in a handler. Whatever the vendor, keep prompts in files under version control with a header (purpose, model, version, last evaluated against what).

### 3.4 Tokens, the context window and caching

A token is roughly three quarters of an English word; pricing is per million tokens, in three classes — input, output (several times input) and **cached input** (a fraction of input) — per Cursor's explainer (2025-09). The context window is a hard per-model limit that *everything* shares: system prompt, tool definitions, history, attached files, tool results. Quality degrades before the limit — "lost in the middle": material in the middle of a long context is recalled worse than the start or the end (Pocock, 2025-10, citing the paper). Practical rules: know the window of the model you use; start a new thread or session when the topic changes instead of letting stale context contaminate answers (Ng; Pocock's `/clear` over `/compact`); audit tool and MCP schemas because they load every turn (`07-token-economy.md`).

**Prompt caching is prefix caching.** The vendor caches a stable, append-only prefix; the first variable token breaks the cache for everything after it. Order the request static-first — system instructions, tool definitions, reference material, examples — and dynamic-last — conversation, the current input. With that order, a multi-turn feature pays full price for the prefix once and the cached price afterwards; without it, the cache never hits and the bill and latency show it. This is the cheapest token lever in the KB and was missing from `07` until this scan.

### 3.5 Providers: choose by checklist, keep switching cheap

The labs' top models are near parity and rotate quarterly (`08-model-selection.md`); the durable differences are in the API. Choose a provider on observable criteria — the API shape(s) it speaks, whether a reasoning tier exists, prompt caching and its rules, structured outputs / JSON-schema enforcement, tool calling and hosted tools, MCP support, state options and zero-data-retention / encrypted reasoning, rate limits and regions, price per million tokens per class, and how much of your code changes if you swap. Each lab now owns its own API shape, with an open standard (Open Responses, 2026-01) trying to make one shape common for open-weight servers and the Claude Messages API observed as a compatibility target for third-party servers at that date (Witteveen). The cheap protection is a **thin wrapper of your own** — one module that owns the model name, the call, timeouts, retries, usage logging and the item-list format — rather than a heavyweight abstraction framework: switching becomes a config change plus one adapter. Consumer "which $20 plan" comparisons answer none of these questions. Checklist: `practices/llm-api-calls/provider-selection-checklist.md`.

## 4. How to apply it in a repo

1. Confirm the fact `llm_calls` (`practices/facts.md`); if the product calls a model at runtime, `practices/llm-api-calls/` applies.
2. Create one client module from `practices/llm-api-calls/llm_call_skeleton.py`: model name, max tokens, timeout, retries, usage logging and the item-list loop in one place; no vendor SDK calls anywhere else.
3. Move every runtime prompt into a versioned file built from `system-prompt-template.md`, static sections first, with a header (purpose, model, version, last evaluated).
4. For each prompt, write ten real inputs and five edge cases; run them N times; read the outputs; fix the prompt; repeat. Record what changed in the prompt header.
5. Walk `failure-modes-and-mitigations.md`: for each failure mode that applies (character-level tasks, arithmetic, fresh facts, policy-bound answers, irreversible actions), name the tool, retrieval or deterministic check that covers it.
6. Fill `provider-selection-checklist.md` once; keep it in `docs/` next to the model policy from `08-model-selection.md`.
7. Verify prompt caching hits: log cached-input tokens per call; a multi-turn feature with zero cached tokens has its prompt in the wrong order.

## 5. Anti-patterns

- Asking the model for a fact, identifier, date or number it "should know" instead of putting the source in the context or calling a tool.
- Requiring a bare final answer ("reply with just the number") on a multi-step problem, or hand-scaffolding "step 1, step 2" on a reasoning model that has a native thinking budget.
- Prompting around character counting, string slicing or arithmetic instead of giving the model a code tool.
- Guarding an irreversible action with a second model's opinion and calling it verification.
- Reporting an aggregate pass rate on an eval where one flaky scenario out of ten ships to users.
- Prompts as string literals in handlers, edited in place, never versioned, never tested on edge cases.
- Variable content (date, user name, session id) at the top of the system prompt — the prompt cache never hits.
- Choosing a provider from a consumer plan comparison, or wrapping the vendor SDK in a framework so large that switching means a rewrite.

## 6. Evidence & sources

- Digest with the impact table — `sources/2026-09-27-s01-llm-setup-digest.md`; scan log with the 13 selected and 94 discarded items — `sources/2026-09-27-market-scan-s01-llm-setup.md`.
- Mechanism (compression, tokens, fixed compute per token, RL on verifiable rewards, Swiss cheese): Karpathy, *Deep Dive into LLMs like ChatGPT* (2025-02) and *Intro to Large Language Models* (2023-11), transcripts in `sources/raw/2026-09-27-market-scan-s01-llm-setup/`.
- Plausibility engines, correlated failures, per-scenario consistency: Dan Klein on *Chain of Thought* (2026-04); the second half of the episode is a product pitch and is not used.
- Call structure, state, reasoning items, caching, hosted tools, prompt objects: OpenAI *Build Hour: Responses API* (2025-10); Anthropic *Building with MCP and the Claude API* (2025-10).
- Prompt structure and craft: Anthropic *Prompting 101* (2025-05) and *AI prompt engineering: a deep dive* (2024-09); JetBrains (2026-02); DeepLearning.AI / Andrew Ng *Full AI Prompting Course* (2026-05) for sycophancy, staged generation and the "think step by step" caveat.
- Tokens and context: Cursor *Tokens & Pricing* (2025-09); Matt Pocock *How context windows work* (2025-10).
- Standards and providers: Sam Witteveen *Open Responses* (2026-01); IBM *What is an AI stack?* (2025-11, vocabulary only).
- Written canon for the same topic (Claude, OpenAI, Gemini platform docs; Chip Huyen; Lilian Weng; Applied LLMs) is catalogued in the Claude Project doc `curso-fuentes-sesiones-01-05.md`; promote this principle to `current` after checking §3.2 and §3.4 against the vendors' current docs and LIDR session 1.

## 7. Change log

- 2026-09-27 — created from `sources/2026-09-27-s01-llm-setup-digest.md` (market scan for LIDR session 1). Status `draft` until the session on 2026-10-15.
- 2026-09-27 (s2) — reviewed against `sources/2026-09-27-s02-context-caching-digest.md`: §3.4 caching rule confirmed and sharpened with the break list (timestamp, cwd or user name at the top; tool list changing per turn; edits to earlier messages; compaction — expected); minimum cacheable prefix ~1,024 tokens and TTLs of 5 min–1 h recorded in the practice; §3.3 gains "positive examples over negative rules; route or phase-swap instead of one growing prompt" (Anthropic's post via Ebbelaar). Multi-turn context management is `11-runtime-context-management.md`.
- 2026-09-30 (s3) — refined against `sources/2026-09-30-s03-wrappers-digest.md`: the client module's retry on 429/5xx is for a single service; in production the retry owner moves to the gateway layer (`12-llm-gateway-layer.md`) and the SDK's retries go to 0 — stacked retries reached 16 attempts per call at ManyChat. Model ids move from the module constant to a registry with a daily availability check. Store structured prompt inputs and the prompt version, not only the rendered string, so a call can be replayed (TensorZero). Provider checklist row 8: a gateway's data policy (no logging by default) does not override the upstream provider's retention/training policy — both apply.
