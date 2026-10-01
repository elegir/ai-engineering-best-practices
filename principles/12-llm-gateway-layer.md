---
title: "The LLM gateway layer — fallback over retry, one owner of retries, cooldown and timeouts per route, streaming as a pipeline, tracing as distributed tracing, and the narrow place of a semantic cache"
type: principle
status: draft              # draft until LIDR session 3 (2026-10-29) confirms or contradicts
date: 2026-09-30
last-reviewed: 2026-10-01
tags: [llm-gateway, routing, fallback, retries, cooldown, timeouts, streaming, sse, observability, opentelemetry, semantic-cache, model-registry, s3]
sources:
  - sources/2026-09-30-s03-wrappers-digest.md
  - sources/2026-09-30-market-scan-s03-wrappers.md
  - https://docs.litellm.ai/docs/routing
  - https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md
  - https://github.com/humanlayer/12-factor-agents
supersedes: null
superseded-by: null
---

# The LLM gateway layer

## 1. The question this answers

Once a product calls models from more than one place, or depends on them in production, what belongs in the layer between the application code and the providers — routing, fallback, retries, timeouts, keys, streaming, tracing, caching, model lifecycle — how is each of those done so that an outage, a rate limit or a retired model does not become an incident, and what does *not* belong there?

## 2. Short answer

Put one **gateway layer** — a library in each service or a small shared deployment, never a single company-wide choke point — between your code and the providers, and give it exactly these jobs. **Route and fall back**: on failure go to the *next deployment*, not the same endpoint again; keep **one owner of retries** with a small cap and jitter; put failing deployments in **cooldown**; set **timeouts per model class and route** (a reasoning model's normal is a chat model's outage); keep fallbacks **pre-approved and evaluated** — same model via other capacity is transparent, a different model is a product change; size capacity in **tiers** (reserved → pay-as-you-go → direct providers at weight 0) and when quota runs out **route, don't scale, bound the queue, shed by priority**. **Scope keys** per route and tenant with spend caps. Keep a **model registry** with a daily availability check, because retirements are announced and still break hardcoded ids. **Stream** through the layer as a pipeline of stages (timeout → token count → guardrail buffer → SSE decode → finish check), SSE at the edge, and fall back only before the first token. **Trace** every call as an OpenTelemetry span with the GenAI attributes, content opt-in, secrets redacted, and build the dev loop on replaying traces; page on deterministic expectations, never on judge scores. Keep a **semantic cache** out of the layer unless the content is stateless, non-personal and slow-changing, and then only behind tenant/domain/version filters and a conservative threshold. Everything else — prompts, context assembly, control flow, tool dispatch — stays in your code, owned and versioned (12-Factor Agents); the gateway is plumbing, not intelligence.

## 3. Long explanation

### 3.1 What the layer is, and the two tensions

A gateway is a server or library between application code and model providers that handles the provider-interface mismatch, retries, fallbacks, load balancing, credentials, caching, accounting and observability — "one endpoint instead of five SDKs" (TensorZero; `sources/2026-09-30-s03-wrappers-digest.md` §3.1). It exists to manage a trade-off that cannot be maximised on all sides: **availability, latency, guardrails and cost** (Twilio); during a degradation you choose which to give up, per route, in advance. It is the client module of `10-llm-api-fundamentals.md` §3.5 grown to serve several services and several providers, and the design stance does not change: own your prompts, your context window and your control flow; tools are "just JSON and code"; the agent is a stateless reducer over state you own (12-Factor Agents). The gateway normalises transport; it does not think.

Two tensions the sources leave open. **Central or decentralised?** Vendors describe one central place for credentials, caching opt-ins, accounting and data policy (TensorZero, OpenRouter); Twilio argues a company-wide gateway is a single point of failure and that teams want *centralised governance, not centralised traffic* — the layer as a library or per-team deployment, with plugins that centralise cost tracking and limits. For a solo owner with a handful of products the fit is a library in each service with one shared configuration (an opinion, stated as such). **Is the gateway also an optimisation platform?** TensorZero's thesis — every LLM call a typed function whose prompt/model *variants* can be A/B-tested and fine-tuned — is a vendor hypothesis without a benchmark. The KB keeps its storage half: store the structured inputs and the prompt version, not only the rendered string, so a call can be replayed and later re-templated.

### 3.2 Fallback, retries, cooldown, timeouts, capacity, keys, lifecycle

- **Fallback over retry.** An LLM call is slow and expensive; retrying the same endpoint burns the latency budget and multiplies cost and tail latency. Try deployment A, then B (Twilio; ManyChat: "increasing retries doesn't work in this use case"). Parallel fan-out doubles cost — a premium per-route option, never a default.
- **One owner of retries.** ManyChat set 3 retries + the first try at the router *and* retries in the agent framework: up to **16 attempts per call**, in synchronised waves that delayed recovery. Audit every layer (SDK, framework, router, gateway); one owner; small cap; jitter; retries capped as a share of normal flow; 429 waits (`retry_after`), 400 never retries.
- **Cooldown, not circuit breaker.** A deployment that crosses `allowed_fails` within a minute leaves the pool for `cooldown_time` seconds, then is re-tried (LiteLLM; Writer's ~5-minute latch). Decide where the counters live: per-instance counters shift the failover threshold silently under autoscaling; shared counters (Redis) fail over faster at the price of shared infrastructure.
- **Timeouts per model class and route.** Without one "your gateway thinks your request is being happily served while it is not" — the top cause of silent outages (Twilio). Chat ~3 s, embeddings < 1 s, reasoning 2–60 s on the same prompt; track p99 per model per route, never gateway-wide; pin the reasoning-effort parameter per route and treat auto-select models as latency risk.
- **Fallbacks are not transparent.** "OpenAI-compatible" providers differ in tool-calling schemas, token limits, stop reasons and JSON-mode support; a provider error can surface through a gateway as an opaque 400 (TensorZero's Anthropic example). Log the raw provider request, response and error body at the layer; run the same eval through every fallback target. Same model via other capacity is transparent (ManyChat's tiers); a different model "needs an evaluation system" and changes the product — **available is not approved** (API World): fallback targets are pre-decided against data sensitivity, consequence, capability and cost, never chosen mid-incident.
- **Provision the fallback at primary volume** and load-test it; it is the last line of defence and the least tested (Twilio).
- **Tiers and shedding.** ManyChat under a 10× viral spike (≈30 → 300 RPS): reserved capacity sized just above baseline at 80 % weight, pay-as-you-go at 20 % (kept warm), direct providers at weight 0 used only on 429/failure — sustained at ~1.5× baseline cost, no pages (self-reported). Provider quota is rented, so pods do nothing against 429s: "we don't scale it, we route it with what we have". Excess has three destinations — queue, raise the cap (cost), drop by priority; "queues absorb short spikes but not lasting overload", so bound the queue and attach a deadline (ManyChat admitted an unbounded queue and no way to cancel abandoned requests; Twilio: load shedding belongs in the runbook).
- **Keys and spend.** Keys per route and per tenant so one noisy tenant cannot exhaust everyone's quota (Twilio); per-key spend caps and anomaly alerts — a gateway "is a target for fraud", and a runaway agent hits the bill the same way as a stolen key (OpenRouter).
- **Model lifecycle.** A model id hardcoded in ~22 places, a retirement the vendor had announced, no alert, a broken production button: "information is not control". One source of truth for model ids; a daily check of the provider's model list against the ids in use; an alert on mismatch *and* on the check failing; re-audit the older systems, which is where it broke (API World). Re-evaluate model choice quarterly — the market "swings": frontier launch → usage surge → invoices 30 days later → a cheaper option months later (OpenRouter) — and never hardcode a model or a price into product logic (`08-model-selection.md`).

### 3.3 Streaming through the layer

SSE is the default edge transport for token streaming: text over HTTP, one-way, auto-reconnect, stateless so a reconnect lands on any server; WebSockets need stateful scaling and are for client→server streams (voice, collaboration); gRPC bidirectional streaming stays internal because browsers cannot read trailers and gRPC-Web needs a proxy; Protobuf for service contracts, JSON wherever a model reads the payload (CNCF panel; Writer). Parse correctly: `data: <json>` lines split across network chunks, so buffer and reassemble; the `[DONE]` sentinel separates a finished stream from a dropped connection (Writer). Build clients on **typed events**, never regex over text deltas (OpenAI, s1); a structured route streams typed *partial objects* (a growing, validated object) or *iterable* objects (one complete object at a time), not text deltas, and the renderer consumes fields (Liu, 2024-09; `principles/13-structured-outputs-and-guardrails.md` §3.1). The layer's stream is a **pipeline of stages**: timeout → token counting and metrics → buffering for guardrails (token-level filtering is meaningless; buffering delays first visible output, so the buffer size is a per-route decision) → SSE decode → `finish_reason` check. **Fallback inside a stream happens before the first token**: wait for it to classify error vs response, then commit; after tokens were shown, switching provider needs a product decision (discard or splice) — this is why "something went wrong, please try again" exists (Twilio). Guardrail placement is a per-route attribute: pre-hooks are safest and add serial latency; parallel guardrails save latency but do not combine with streaming; post-hooks suit auditing; each guardrail has a fail-open or fail-closed policy and a time budget so the model stays the rate-determining step (Twilio). Guards on side effects run **blocking** at the tool boundary — the tool never executes until the check passes (the OpenAI Agents SDK makes this an input-guardrail option, `run_in_parallel=False`; its output guardrails always run after the output exists — page read 2026-10-01); the allowance that guards on user-visible text may run parallel on non-streamed routes is Twilio's (above). The checkpoints are input, retrieval, tool call, output, memory and plan (NeMo Guardrails' five rails; Carpintero, 2026-04); content, tiers and on-fail actions per checkpoint are in `practices/structured-outputs/guardrail-policy.md`, which closes the s3 park on the placement table in `practices/llm-gateway/routing-policy.md` §Guardrails. Streams are opaque to WAFs, so injection checks live in the application layer.

### 3.4 Traceability

"LLM observability isn't a different problem from distributed tracing — it's a special case of it" (Langfuse). An LLM call is a span, a pipeline is a trace, context propagates with `traceparent`, and the same collector carries it to whatever backend. The OpenTelemetry GenAI conventions (status **Development** on 2026-09-30 — pin instrumentation versions, expect names to move): span name `{gen_ai.operation.name} {gen_ai.request.model}`; attributes `gen_ai.operation.name`, `gen_ai.provider.name`, `gen_ai.request.model`, `gen_ai.response.model`, `gen_ai.response.id`, `gen_ai.response.finish_reasons`, `gen_ai.conversation.id`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.usage.cache_read.input_tokens`, `gen_ai.usage.cache_write.input_tokens`, `gen_ai.usage.reasoning.output_tokens`, `gen_ai.request.reasoning.level`, `gen_ai.prompt.version`, `gen_ai.tool.*`; content (`gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.system_instructions`, `gen_ai.tool.definitions`) is **opt-in**. Practice (Langfuse and Arize founders; PyCon DE): start with traces, then evals — offline evals are unit tests, online evals are monitoring, production cases feed the offline set; the P0 workflow is trace → replay in a playground → edit → re-run, so the store must capture the full prompt, tool definitions and inputs; sampling is rare and retention is the cost lever; page on deterministic expectations with ordinary alerting, never on LLM-judge scores; filter infrastructure spans; put a session id and a *pseudonymous* user id on the root span; a gateway traces only its own segment unless callers forward context. One hazard: auto-instrumentation records function arguments by default — a client object in a traced function puts the API key in the trace store. OTel alone does not make you vendor-agnostic ("still a lot of monkey-patching"), but it lets you switch backends with a mapping layer. This extends `21-agent-design-and-tools.md` §3.3 and `practices/context-management/context-metrics-and-evals.md` with the standard names.

### 3.5 Semantic caching, narrowly

A semantic cache embeds the query, finds a stored query above a similarity threshold and returns *that* query's answer — someone else's answer. It is therefore safe only for stateless, non-personal, slow-changing content (an FAQ, documentation), behind tenant, domain, language and model/prompt-version filters, a short TTL for anything that changes, and a conservative threshold (90–95 %): the vendor demo's 85 % returned a different question's answer on the speaker's own example (the language Python vs the snake), while 95 % would have rejected a legitimate 90 % paraphrase — the useful band is narrow and per-domain (Percona/Valkey; numbers are the vendor's). It is unsafe for personalised, tenant-scoped, time-sensitive or tool-using responses, and a cross-user cache without tenant keys leaks one user's context into another's. It sits *above* provider prompt caching (`11-runtime-context-management.md` §3.3), which caches the prefix of *your own* request and never returns another request's output. The one caching use nobody disputes: cached responses in test pipelines, because live LLM tests are flaky (ManyChat).

### 3.6 The interface

The conversational UI (Streamlit, Gradio, a web front end) holds **no model logic**: it renders typed events from the layer and keeps session state — and, where the user and the agent work on one artifact, typed state *both ways*: state snapshots and deltas from the agent, a human edit back as agent context (CopilotKit's AG-UI demonstrations, 2026-01; `principles/13-structured-outputs-and-guardrails.md` §3.5); swapping the UI must not touch a prompt. The Streamlit chat docs and Gradio's `gr.ChatInterface` are the canon (`sources/catalog-written-canon.md` §Session 3).

## 4. How to apply it in a repo

1. Confirm `llm_calls` and `production` (`practices/facts.md`); if both hold, `practices/llm-gateway/` applies. Below production, `practices/llm-api-calls/` alone is enough.
2. Copy `gateway_config.yaml` and fill it per route: deployments and weights, `allowed_fails`/`cooldown`, timeout per model class, retry owner and cap, reasoning level, streaming on/off, guardrail placement.
3. Decide every fallback with `fallback-approval.md` — same-model vs cross-model, data sensitivity, evals run — and write the decision into the config comments.
4. Scope keys per route and tenant; set spend caps and an anomaly alert (`security-baseline/` key row).
5. Create the model registry from `model-registry.md`; schedule the daily availability check; alert on mismatch and on check failure.
6. If a route streams, build it from `streaming-pipeline.md`: SSE at the edge, pipeline stages, first-token fallback, `[DONE]` handling, typed events to the UI.
7. Instrument with `tracing-otel.md`: GenAI attributes, content opt-in, redaction, session and pseudonymous user ids; verify a trace can be replayed.
8. Only if the content qualifies, add a semantic cache from `semantic-cache-decision.md`, with filters, TTL and a measured false-positive check.
9. Game-day the layer: kill the primary deployment, hit the rate limit, retire a model id, drop a stream mid-way — and read the traces.

## 5. Anti-patterns

- Retrying the same endpoint five times with no jitter, in two layers at once.
- One global timeout for chat, embeddings and reasoning routes.
- A fallback to a different model that nobody evaluated, chosen during the incident.
- Scaling pods against a provider's 429s; an unbounded queue with no deadline.
- One shared API key for every route and tenant; no spend cap.
- A model id string in twenty files; no check that it still exists.
- Switching provider after tokens have reached the client and splicing the output.
- Regex over text deltas instead of typed events; token-level guardrails on a stream.
- Prompts and completions in traces by default; API keys captured by a tracing decorator; paging on an LLM-judge score.
- A semantic cache in front of personalised or tenant-scoped answers, or at an 85 % threshold because the demo used it.
- A company-wide gateway everything depends on, with no library mode.

## 6. Evidence & sources

- Digest with the impact table — `sources/2026-09-30-s03-wrappers-digest.md`; scan log — `sources/2026-09-30-market-scan-s03-wrappers.md`; written canon — `sources/catalog-written-canon.md` §Session 3.
- Fallback, retries, timeouts, tiers: Kanish Manuja, Twilio (AI Engineer, 2026-06); Sergi Porta, ManyChat (EuroPython, 2026-08); Isadora Martin-Dye (API World, 2026-09); Viraj Mehta, TensorZero (AI Engineering Podcast, 2025-01); LiteLLM Router docs (read 2026-09-30).
- Streaming: Writer (Scala Days, 2025-11); CNCF panel (2026-02); OpenAI Build Hour (s1, reused).
- Tracing: Langfuse (2026-07); Klingen & Lopatecki (Mastra, 2025-12); Emanuel Fabani (PyCon DE, 2025-10); OpenTelemetry GenAI span conventions (`semantic-conventions-genai`, Development, read 2026-09-30).
- Semantic caching: Martin Visser (Percona/Valkey, 2026-01); Redis canon pages.
- Design stance: Dex Horthy, 12-Factor Agents (AI Engineer, 2025-06; repo).
- Market: OpenRouter on Latent Space (2026-09; low engineering content, used for the price swing, data policy and fraud only).

## 7. Change log

- 2026-09-30 — created from `sources/2026-09-30-s03-wrappers-digest.md` (market scan for LIDR session 3). Status `draft` until the session on 2026-10-29.
- 2026-10-01 (s4) — refined against `sources/2026-10-01-s04-structured-outputs-digest.md`: §3.3 — a structured route streams typed *partial objects*, not text deltas (Liu 2024); guards on side effects run **blocking** at the tool boundary (Agents SDK 2026-10-01: `run_in_parallel` is an input-guardrail option; output guardrails run after completion), the parallel allowance for text guards stays Twilio's; the checkpoint list (input, retrieval, tool, output, memory, plan — NeMo, Carpintero) and the placement table now point to `practices/structured-outputs/guardrail-policy.md` for content, tiers and on-fail actions (closes the s3 park). §3.6 — the UI consumes typed events *and typed state, both ways* (AG-UI).
