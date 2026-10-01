# Stack-notes — PHP / Laravel

Written 2026-09-30. Core and full parts per `README.md`.

- **Secret scan:** gitleaks is language-independent; add `bootstrap/cache/` and `storage/*.key` to the protected paths because `config:cache` and Passport write secrets there.
- **Dependency audit (assertion 3):** `composer audit` fails on any advisory by default; to approximate "high or critical only" use `--ignore-severity=low --ignore-severity=medium` (Composer ≥ 2.8, 2024-10) and say so in the policy; run it in pre-push via lefthook.
- **Where secrets live:** `.env` only; `config/*.php` reads them with `env()`; anything else (`env()` in a controller) is a finding.
- **Injection fixture (assertion 5):** the fixture page is the same; the eval runs through whatever agent loop the product has (often none — then the fixture tests the *coding* agent, which still applies).
- **MCP trust register:** Laravel repos often reach the database through an MCP in Claude Desktop; register it as read-only and name the production connection as out of scope.
- **Per-tenant keys (assertion 8):** encrypted columns (`Crypt::encryptString`), rotated by a command, spend cap enforced in the gateway class with `Cache::increment` per tenant per day.
- **Pitfall:** `php artisan tinker` in a session with production credentials is a destructive command in disguise; deny `tinker` when `APP_ENV=production`.
