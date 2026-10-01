# Stack-notes — PHP / Laravel

Written 2026-09-30 before the first Laravel adoption (decision 0005 §10, arm b of the experiment). Package families verified to exist on Packagist on this date; versions and defaults must be checked at adoption — this note names *which* to look at, not what version.

- **Package family (choose one, record the choice in `docs/llm-provider.md`):** (a) the vendor's official PHP SDK — Anthropic publishes `anthropic-ai/sdk` (GitHub `anthropics/anthropic-sdk-php`; check its beta status); OpenAI has the community-maintained `openai-php/client` with a `openai-php/laravel` service provider; (b) a Laravel-native layer such as Prism (`prism-php/prism`, prismphp.com) that wraps several providers with one API. Rule from assertion 1: whichever is chosen, exactly one class in `app/` instantiates it.
- **Retries (assertion 4):** check whether the chosen package retries internally and whether Laravel's HTTP client `retry()` is also in play; pick one owner. In Laravel the right owner for a slow or rate-limited call is usually a **queued job with backoff** (`$backoff`, `$tries`), not the request.
- **Names that differ from the Python reference:** `max_tokens` → the same; `system` → a `system` parameter or a `SystemMessage`; usage fields come back as arrays or value objects, not attributes — map them once in the client class.
- **Prompt files:** `resources/prompts/<id>.md` with the header block; load with `File::get()` and cache with the config cache, never by `include`.
- **Prompt caching (assertion 3):** only works if the client sends the `cache_control` blocks (Anthropic) — confirm the package exposes them; if it does not, this is a reason to prefer the official SDK.
- **Runtime:** PHP-FPM is request-scoped — no module-level singleton survives; bind the client in the service container as a singleton *per request* and keep any cooldown state in `Cache::`.
- **Streaming:** needs `response()->stream()` and a server that does not buffer; most shared hosts buffer. Default to non-streaming plus a queued job unless the product needs tokens on screen.
- **Pitfall:** `config:cache` freezes `env()` calls — read the API key through `config('services.anthropic.key')`, never `env()` outside `config/`.
