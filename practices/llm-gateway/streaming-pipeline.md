# Streaming through the layer — transport, pipeline stages, failure points

Copy into `<repo>/docs/llm-gateway.md` §streaming. Principle: `../../principles/12-llm-gateway-layer.md` §3.3. Sources: Writer (Scala Days, 2025-11), CNCF panel (2026-02), OpenAI Build Hour (s1), Twilio (2026-06) — `../../sources/2026-09-30-s03-wrappers-digest.md` §3.3.

## Transport

| Hop | Use | Why |
|---|---|---|
| Browser / client ← edge | **SSE** (Server-Sent Events) | text over HTTP, one-way, auto-reconnect, stateless (a reconnect lands on any server); works through CDNs and enterprise firewalls |
| Client → server streams (voice, collaboration) | WebSocket | only when the client streams *to* you; needs sticky/stateful scaling |
| Service ↔ service, service ↔ vector DB / model server | gRPC bidirectional (internal only) | flow control, typed contracts; browsers cannot read trailers; gRPC-Web needs a proxy |
| Payload encoding | Protobuf for service contracts; JSON wherever a model must read it | never feed raw protobuf to a model |

HTTP/3 and WebTransport exist; enterprise firewalls drop UDP; SSE over HTTP/2 through the CDN is the pragmatic choice (2026-02).

## The stream as a pipeline (one stage per responsibility, in this order)

```
provider stream
  → timeout stage          (per-route timeout; also time-to-first-token budget)
  → token count + metrics  (input/output/cached tokens, TTFT, inter-token latency → trace span)
  → guardrail buffer       (token-level checks are meaningless; buffer <<n>> tokens / sentence boundaries, run the check, release)
  → SSE decode / re-encode (reassemble `data: <json>` lines split across network chunks; typed events out)
  → finish check           (`finish_reason` / stop reason present? `[DONE]` sentinel received? else → error, not success)
  → client
```

- **Typed events to the UI** (item added · text delta · tool-call delta · item done · error · done), never regex over text deltas (OpenAI Responses / Anthropic Messages both stream typed events). The UI holds no model logic.
- **`[DONE]` (or the provider's terminal event) separates a finished stream from a dropped connection.** A stream that ends without it is a failure to log and to surface, not a short answer.
- **The guardrail buffer delays first visible output** by its size — a per-route number, written in the config. Parallel guardrails do not combine with streaming; use pre-hooks (serial) or buffered post-checks.

## Failure points

| When | What the layer does |
|---|---|
| Error before the first token (5xx, 429, timeout on TTFT) | Fall back silently to the next deployment; the client never sees it (Writer waits for the first token to classify error vs response) |
| Error after tokens reached the client | **Product decision, decided before launch**: (a) keep the partial text and show "something went wrong, please try again" (default); (b) discard and restart on another deployment, telling the user; (c) splice — only if the output is append-only and the prompt is deterministic enough. Twilio: once tokens reach the client you cannot switch provider transparently |
| Client disconnects | Cancel the upstream request (stop paying for tokens nobody reads); record the cancel in the trace |
| Guardrail trips mid-stream | Stop the stream, emit a typed `error`/`blocked` event with the partial text handling defined per route |

## Metrics to emit per streamed call

`time_to_first_token`, `inter_token_latency_p50/p99`, `stream_duration`, `tokens_out`, `terminated_by` (done / error / client_cancel / guardrail), `fallback_used` (deployment id), plus the GenAI span attributes (`tracing-otel.md`).

## Minimal stage skeleton (pseudocode; the shape matters, not the language)

```
async def stream_route(route, request):
    with span("chat {model}", gen_ai attrs...):
        for deployment in route.deployments_in_order():
            try:
                upstream = await deployment.open_stream(request, timeout=route.timeout_ttft)
                first = await upstream.first_event()            # classify here: error → next deployment
                break
            except (ProviderError, Timeout):
                mark_cooldown(deployment); continue
        else:
            raise AllDeploymentsFailed
        async for ev in guardrail_buffer(count_tokens(upstream_with_timeout(upstream, route.timeout)), route.buffer_tokens):
            yield typed_event(ev)                                # text_delta / tool_call_delta / item_done
        if not upstream.finished_cleanly():                      # no finish_reason / [DONE]
            yield typed_event(error="stream dropped")
        yield typed_event(done=True)
```
