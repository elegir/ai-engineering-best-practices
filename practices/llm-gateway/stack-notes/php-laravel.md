# Stack-notes — PHP / Laravel

Written 2026-09-30 (no Laravel adoption yet). Check at adoption.

- **Where the gateway lives:** for a request-scoped app, prefer a **hosted gateway** (a vendor router, LiteLLM as a sidecar) over an in-app gateway; the in-app option works only if every piece of state below is externalised.
- **Cooldown and circuit state** (assertion 2): `Cache::` with the framework's atomic locks — never a static property, which resets on every request and makes the assertion pass in `tinker` and fail in production.
- **Retries:** a queued job with `$tries`/`$backoff` is the single retry owner; the HTTP client's `retry()` must then be off.
- **Model registry** (assertion 3): one `config/llm.php` file; the daily id check is a scheduled command (`schedule:run`).
- **Streaming** (assertion 5): server-sent events need output buffering off and a non-buffering web server; test on the real host, not on `artisan serve`.
- **Tracing** (assertion 6): the OpenTelemetry PHP SDK exists; the GenAI attribute names are identical to Python's. Redact before export — Laravel's request logging captures bodies by default in some packages.
- **Keys per tenant** (assertion 8 of `security-baseline`): store per-tenant keys encrypted (`Crypt::`), resolve them in the gateway class, never in controllers.
