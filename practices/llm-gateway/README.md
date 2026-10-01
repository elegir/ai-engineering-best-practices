---
title: "Practice — LLM gateway layer: routing and fallback policy, per-route config, fallback approval, model registry, streaming pipeline, OpenTelemetry tracing and the semantic-cache decision"
type: practice
status: draft            # draft until principle 12 is confirmed against LIDR session 3
date: 2026-09-30
last-reviewed: 2026-09-30
tags: [llm-gateway, routing, fallback, retries, timeouts, streaming, observability, opentelemetry, semantic-cache, model-registry]
kind: capability
applies-when: "llm_calls and production"
principle: principles/12-llm-gateway-layer.md
sources:
  - sources/2026-09-30-s03-wrappers-digest.md
  - https://docs.litellm.ai/docs/routing
  - https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md
supersedes: null
superseded-by: null
---

# LLM gateway layer

## Solves
The product depends on model providers in production and one of these symptoms appears: a provider's 429s or a slow reasoning model become an outage because there is no fallback, no per-route timeout or no cooldown; retries exist in two layers and multiply under load; a fallback to a different model was picked during an incident and changed the product's behaviour; one shared API key serves every route and tenant; a model id lives in twenty files and a retirement broke a button; streams switch provider mid-way or are parsed with regex; traces are missing, or contain prompts and API keys by default; a semantic cache answers one user's question with another user's answer.

## Applies when
- The facts `llm_calls` and `production` hold (`../facts.md`): the product calls a model at runtime and real users or third parties depend on it now — including scheduled systems with no UI that email, publish or sync.
- Several services or several providers are in play, or a single service whose availability matters.

## Does not apply when
- Below production (a prototype, an internal tool with one user): `../llm-api-calls/` alone — its client module already centralises model name, timeout and retries for one service.
- The only model in the picture is the coding agent working on the repo.
- Guardrail *content* (what to check, with which validator) — session-4 practice (pending); this folder decides only *where* a guardrail runs and how it fails.
- Self-hosted inference (KV-cache-aware balancing, GPU scheduling) — session 15 (pending).

## Files in this folder
| File | Copy to | Purpose |
|---|---|---|
| `routing-policy.md` | `<repo>/docs/llm-gateway.md` | The rules, one per decision: fallback over retry, one retry owner, cooldown, timeouts per class, tiers, queue bound and shedding, keys and spend caps, guardrail placement and fail policy, first-token fallback for streams |
| `gateway_config.yaml` | `<repo>/config/llm-gateway.yaml` (LiteLLM Router shape; map to your router) | Per-route deployments, weights, `allowed_fails`/`cooldown_time`, `timeout`, `num_retries`, reasoning level, streaming, guardrails — with every number marked and dated |
| `fallback-approval.md` | one block per fallback, in `docs/llm-gateway.md` | "Available is not approved": same-model vs cross-model, data sensitivity, consequence, capability, evals run, who approved, when |
| `model-registry.md` | `<repo>/docs/models.md` + a daily job | Single source of truth for model ids; the daily availability check; alert on mismatch and on check failure |
| `streaming-pipeline.md` | `<repo>/docs/llm-gateway.md` §streaming (+ the stage skeleton) | SSE at the edge, stage pipeline (timeout → tokens → guardrail buffer → decode → finish check), `[DONE]`, first-token fallback, typed events to the UI |
| `tracing-otel.md` | `<repo>/docs/observability.md` §llm | The GenAI span attributes to emit, content opt-in, redaction, session and pseudonymous user ids, replay requirement, what to page on |
| `semantic-cache-decision.md` | the feature spec | Whether a semantic cache is allowed at all for this route; filters, threshold, TTL, false-positive check |

## Adapt
- `gateway_config.yaml`: it is written in LiteLLM Router terms because that is the most widely used open router; OpenRouter, Vercel AI SDK, a hand-written router or a vendor gateway have the same knobs under other names — keep the *decisions* (one owner of retries, cooldown per deployment, timeout per class, weights, fallback order) and translate the keys. Every number is a placeholder with a date.
- `routing-policy.md`: delete rules for things the product does not do (no streaming → drop the stream rules); keep the fail-open/closed table even with one guardrail.
- `model-registry.md`: the check is a 20-line script against each provider's models endpoint; schedule it where your other daily jobs run.
- `tracing-otel.md`: use the attribute names as given; if your tracing tool (Langfuse, Phoenix, LangSmith) has its own SDK, map its fields to these and keep OTel as the wire format where the tool supports it.
- Central vs library: the default here is a **library in each service with one shared config file**; a shared gateway deployment is a deliberate choice recorded in `docs/llm-gateway.md` with its single-point-of-failure mitigation.

## Verify
- Kill the primary deployment in a test environment: calls complete through the fallback; the usage log shows the deployment switch; no request exceeds the route's timeout.
- Force 429s: the deployment enters cooldown and leaves it; retries counted in the trace never exceed the single owner's cap.
- `grep -rn "<model id>"` finds exactly one definition (the registry); the daily check ran in the last 24 h and would alert on a fake id.
- Every fallback in the config has an approval block; every cross-model fallback has an eval result attached.
- A streamed route: the client receives typed events; a dropped connection (no `[DONE]`) is reported as an error; a 5xx before the first token falls back silently.
- One trace contains the GenAI attributes, no API key, no raw PII, a session id and a pseudonymous user id; the call can be replayed from the trace.
- If a semantic cache exists: the false-positive check (20 near-miss pairs) passes at the chosen threshold; tenant and version are in the filter.

## Sources
`sources/2026-09-30-s03-wrappers-digest.md` §3.1–3.6 and impact table §6; primary texts in `principles/12-llm-gateway-layer.md` §6. Vendor docs to re-read before promoting to `current`: LiteLLM Router and proxy reliability; OpenRouter provider routing; OTel GenAI conventions (Development status).

## Change log
- 2026-09-30 — created from the session-3 market scan (draft).
