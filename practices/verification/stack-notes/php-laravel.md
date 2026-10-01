# Stack-notes — PHP / Laravel

Written 2026-09-30. The contract is `README.md` §Verify; this is how it is usually satisfied in Laravel.

- **Smoke suite (assertion 1):** Pest or PHPUnit feature tests tagged `@group smoke`, run with `vendor/bin/pest --group=smoke --compact`; seed with factories; `RefreshDatabase` on SQLite in memory keeps it under sixty seconds.
- **HTTP surface:** `api-hurl/smoke.hurl` works unchanged against `php artisan serve --port=8001`.
- **Multi-tenant:** every smoke test must set the tenant first (`tenancy()->initialize($tenant)` or the app's equivalent); a test that passes without a tenant does not count toward assertion 1 — add one that asserts cross-tenant reads return nothing.
- **Dry-run switch (assertion 6):** a config value `services.<name>.mode` (`dry|live`) read from the environment; the sender class checks it; `Mail::fake()` / `Http::fake()` in tests assert the absence of the effect; refuse `live` when `app()->environment() !== 'production'`.
- **Stop gate command:** the smoke group above; the full suite stays in CI.
- **Pitfall:** call `vendor/bin/pest` / `vendor/bin/phpunit` directly from `hooks.json` rather than `php artisan test` — one process fewer and the exit code is the runner's own.
