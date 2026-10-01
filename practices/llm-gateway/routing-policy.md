# Routing policy — the rules, one per decision

Copy to `<repo>/docs/llm-gateway.md`. Each rule names the failure it prevents and the source that recounted it. Principle: `../../principles/12-llm-gateway-layer.md` §3.2–3.3. Sources: Twilio (AI Engineer, 2026-06), ManyChat (EuroPython, 2026-08), API World (2026-09), TensorZero (2025-01), Writer (Scala Days, 2025-11), LiteLLM docs — `../../sources/2026-09-30-s03-wrappers-digest.md`.

## Failure handling

1. **Fallback over retry.** On a failure, go to the next deployment in the route's list; retry the *same* endpoint at most <<1–2>> times, with jitter. Retrying burns the latency budget and multiplies cost (Twilio; ManyChat).
2. **One owner of retries.** Only the router retries. The SDK's built-in retries are set to 0; the agent framework's retries are set to 0. (ManyChat: 4 × 4 = 16 attempts per call, in synchronised waves.) Audit: `grep -rn "max_retries\|num_retries\|retries=" src/` must show one non-zero value.
3. **Class-aware retries.** 429 and 5xx: retry/fall back after `retry_after` or backoff. 400/422 (your request is wrong): never retry. Timeout: fall back, do not retry the same endpoint.
4. **Cooldown per deployment.** A deployment that fails more than `allowed_fails` (<<1>>) times in a minute leaves the pool for `cooldown_time` (<<60–300>> s). Counters: <<per instance | shared in Redis>> — written down, because per-instance counters shift the failover threshold when the fleet scales.
5. **Timeouts per model class and route.** <<chat: 20 s · embeddings: 5 s · reasoning: 90 s · batch: 300 s>> — dated; the reasoning value pins the route's `reasoning_effort` too. Alert on p99 per model per route, never on a gateway-wide aggregate.
6. **Fallbacks are pre-approved** (`fallback-approval.md`). Same model via other capacity: automatic. Different model: only if an approval block exists with evals run; never chosen during an incident. Changing the model changes the product.
7. **Log the raw provider exchange** (request, response or error body) at the layer, redacted, so a provider quirk does not surface as an opaque 400.
8. **The fallback is load-tested** at primary volume once a quarter; its quota and rate limits are known.

## Capacity

9. **Tiers.** <<Reserved/committed capacity sized just above baseline: 80 % weight · pay-as-you-go same provider: 20 % (kept warm) · direct second provider: weight 0, used on 429/failure>> (ManyChat's shape; numbers are placeholders).
10. **Route, don't scale.** Provider quota is rented; adding instances does nothing against 429s. The response to a spike is the next tier.
11. **Bounded queue with a deadline; shed by priority.** Max in-flight = <<n>> (from the provider's rpm/tpm); queue length ≤ <<n>>; requests older than <<deadline>> are dropped with a clear error; routes have a priority so the important ones survive a storm.

## Keys and spend

12. **One key per route and per tenant** (never one shared key). Per-key spend cap <<USD/day>>; anomaly alert at <<×2 of the 7-day mean>>; a revoke runbook. Runaway agents and stolen keys look the same on the bill.

## Models

13. **No model id in code.** Ids live in the registry (`model-registry.md`); the daily availability check alerts on a missing model *and* on its own failure.
14. **Quarterly re-evaluation** of model choice per route; prices and names are never in product logic.

## Guardrails (placement and failure policy; content is the session-4 practice)

| Guardrail | Where it runs | Fails | Time budget | Why |
|---|---|---|---|---|
| <<input injection check>> | pre-hook (serial, before the call) | closed | <<200 ms>> | injection must not reach the model |
| <<PII in output>> | post-hook / buffered on streams | closed | <<300 ms>> | must not reach the user |
| <<toxicity / tone>> | parallel with generation (non-streamed routes only) | open | <<300 ms>> | latency matters more than a rare miss |

Rules: every guardrail has a fail-open/closed decision written before launch, a time budget so the model stays the rate-determining step, and its own fallback (a secondary check or a cached decision). Parallel guardrails do not combine with streaming (Twilio).

## Streams (detail in `streaming-pipeline.md`)

15. **Fallback only before the first token.** Wait for the first token to classify error vs response; after tokens reached the client, a provider switch is a product decision (discard and retry, or splice) — default: surface "something went wrong, please try again" with the partial text kept.
16. **Guardrail buffering on streams is a per-route number** (<<n>> tokens): the buffer delays first visible output.
