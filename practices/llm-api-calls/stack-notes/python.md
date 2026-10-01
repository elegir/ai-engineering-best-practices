# Stack-notes — Python (the reference stack)

Written 2026-09-30. The reference `llm_call_skeleton.py` targets the official `anthropic` SDK; the `openai` SDK is the same shape. Check current versions at adoption.

- **Package family:** the vendor's official SDK (`anthropic`, `openai`); avoid an abstraction layer (LangChain, LiteLLM) *inside the product* unless `llm-gateway` decided on it — two layers means two retry owners.
- **Retries:** both official SDKs retry **twice by default** with backoff. Assertion 4 (one retry owner): either keep the SDK's retries and do none in the client, or set `max_retries=0` and own them. Record which.
- **Prompt caching:** Anthropic needs explicit `cache_control` blocks on the stable prefix; OpenAI caches long stable prefixes automatically. Assertion 3 is judged by `usage.cache_read_input_tokens` (Anthropic) / `usage.prompt_tokens_details.cached_tokens` (OpenAI).
- **Thinking / reasoning budgets:** `thinking.budget_tokens` must be below `max_tokens` (the skeleton guards it); reasoning models on the other vendor use `reasoning.effort`.
- **Usage logging:** both SDKs return a `usage` object per call; log it as structured JSON, not as text.
- **Async:** both SDKs ship an async client; a FastAPI handler must use it or offload to a thread, otherwise one slow model call blocks the event loop.
- **Pitfall:** the SDK reads the API key from the environment by name (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`); a key in `.env` that the process does not load gives an "authentication" error that looks like a vendor outage.
