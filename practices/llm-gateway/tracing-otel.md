# Tracing LLM calls with OpenTelemetry — attributes, opt-ins, redaction, replay

Copy to `<repo>/docs/observability.md` §llm. Principle: `../../principles/12-llm-gateway-layer.md` §3.4. Sources: OpenTelemetry GenAI span conventions (`semantic-conventions-genai` repo, status **Development**, read 2026-09-30 — pin instrumentation versions, expect names to move); Langfuse (2026-07); Klingen & Lopatecki (Mastra, 2025-12); Fabani (PyCon DE, 2025-10) — `../../sources/2026-09-30-s03-wrappers-digest.md` §3.4.

## The model

An LLM call is a **span**; a pipeline (retrieve → rerank → generate → tool) is a **trace**; context propagates with `traceparent`; the same collector and OTLP carry it to the backend (Langfuse, Phoenix, LangSmith, your APM). "LLM observability isn't a different problem from distributed tracing — it's a special case of it."

## The span

- **Name**: `{gen_ai.operation.name} {gen_ai.request.model}` (e.g. `chat gpt-x`, `embeddings text-embedding-y`). Kind `CLIENT`.
- **Required**: `gen_ai.operation.name` (`chat`, `embeddings`, `execute_tool`, …), `gen_ai.provider.name`.
- **Request**: `gen_ai.request.model`, `gen_ai.request.temperature`, `gen_ai.request.max_tokens`, `gen_ai.request.reasoning.level` (the exact string sent), `gen_ai.prompt.version` (your prompt file version — `../llm-api-calls/system-prompt-template.md` header), `gen_ai.conversation.id` (session).
- **Response**: `gen_ai.response.model`, `gen_ai.response.id`, `gen_ai.response.finish_reasons`, `error.type` on failure.
- **Usage**: `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.usage.cache_read.input_tokens`, `gen_ai.usage.cache_write.input_tokens`, `gen_ai.usage.reasoning.output_tokens` — this is where the cache-hit verification of `../llm-api-calls/` and `../context-management/` lives.
- **Tools**: `gen_ai.tool.name`, `gen_ai.tool.type`, `gen_ai.tool.call.arguments` / `.result` (opt-in content).
- **Content — opt-in only**: `gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.system_instructions`, `gen_ai.tool.definitions`. Default off in production; on in dev and for sampled sessions with consent; large content goes to external storage with a reference, not into the span.
- **Your attributes**: `app.route` (chat / extract / reason), `app.deployment` (which tier served it), `app.fallback_used`, `app.tenant_id` (hashed), `app.user_id` (**pseudonymous** — never name/email), `app.session_id` on the root span.

## Rules

1. **Instrument before the prototype is "ready"** — ten minutes now; teams that postpone never get there. Traces first, evals second.
2. **Redact.** Auto-instrumentation and decorators record function arguments by default: a client object in a traced function puts the API key in the trace store (seen live at PyCon DE). Audit captured arguments; strip secrets and raw PII before export.
3. **Capture enough to replay.** The P0 workflow is trace → replay in a playground → edit → re-run; that needs the full prompt (or its version + variables), tool definitions and inputs — store structured inputs and the prompt version, not only the rendered string.
4. **Retention before sampling.** Keep 100 % of traces with 15–30-day retention; sample evals, not traces, unless volume forces it.
5. **Page on deterministic expectations** (a checkout that must happen, a required tool call that did not) with ordinary alerting. Never page on an LLM-judge score; judge scores are dashboards and offline regression.
6. **Filter infrastructure spans** (HTTP, DB) out of the LLM view so they do not drown the model spans.
7. **A gateway traces only its segment** unless callers forward `traceparent` and the session id — require it at the API boundary.
8. **Multi-agent = distributed tracing**: same team → one trace; another team's agent → treat as a tool, trace your side.
9. **Offline evals are unit tests, online evals are monitoring**, and production cases feed the offline set (`../context-management/context-metrics-and-evals.md` §2).

## Verify

One real trace shows: the span name and required attributes; token usage incl. cache fields; `app.route` and `app.deployment`; no API key, no raw PII; a session id and a pseudonymous user id; and a replay from the stored inputs reproduces the call.
