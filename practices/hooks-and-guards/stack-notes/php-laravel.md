# Stack-notes — PHP / Laravel

Written 2026-09-30 for the first Laravel consumer (Martin's multi-tenant app); no version pins — check current versions at adoption. Fifteen lines, no code.

| Purpose | Tool | Command |
|---|---|---|
| Format | Laravel Pint (ships with Laravel; PSR-12/Laravel preset) | `vendor/bin/pint {file}` |
| Lint / static analysis | PHPStan via Larastan | `vendor/bin/phpstan analyse {file} --no-progress` (level 5+; raise over time) |
| Unit / feature | Pest (default since Laravel 11) or PHPUnit | `vendor/bin/pest --compact` (fast subset: `--group=unit`) |
| API e2e | Hurl against `php artisan serve` or Sail | `hurl --test tests/api/*.hurl` |
| Browser e2e | Laravel Dusk or Playwright | `php artisan dusk` / `npx playwright test` |
| Hooks | Lefthook (composer or npm) | `lefthook install` |

**Lines for `hooks.json`:** `"format": {".php": "vendor/bin/pint {file}"}`, `"lint": {".php": "vendor/bin/phpstan analyse {file} --no-progress"}`, `"stop_test_command": "vendor/bin/pest --compact --group=unit"`; protected paths to add: `(^|/)bootstrap/cache/`, `(^|/)storage/oauth-.*\.key$`, `(^|/)database/migrations/.*` once merged; deny to add: `artisan migrate:fresh`, `artisan db:wipe`, `artisan migrate:reset`, any `artisan` command with `--env=production`.

**Pitfalls.** (1) `php artisan config:cache` copies `.env` values into `bootstrap/cache/config.php` — protect that folder, and never commit it. (2) `migrate:fresh` drops every table including tenant data; in a multi-tenant app it is the most destructive command the agent can type — deny it outright. (3) Tenant-scoped tests need the tenancy bootstrapped in the test case (`RefreshDatabase` alone leaves global scope); a green suite that never set a tenant proves nothing about isolation. (4) Pint and PHPStan both read config from the repo root (`pint.json`, `phpstan.neon`) — protect both files.
