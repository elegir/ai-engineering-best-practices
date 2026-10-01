# Stack-notes — PHP / WordPress

| Purpose | Tool | Command |
|---|---|---|
| Format | PHP_CodeSniffer (phpcbf) with WordPress Coding Standards | `vendor/bin/phpcbf --standard=WordPress <file>` |
| Lint | phpcs | `vendor/bin/phpcs --standard=WordPress <file>` |
| Static analysis | PHPStan (+ szepeviktor/phpstan-wordpress) | `vendor/bin/phpstan analyse` |
| Unit | PHPUnit (+ WP_Mock or wp-phpunit) | `vendor/bin/phpunit --testsuite unit` |
| Site-level checks | WP-CLI | `wp core verify-checksums`, `wp plugin verify-checksums --all`, `wp site health` (if available) |
| E2E | Playwright against a local WP (wp-env or Docker) | `npx playwright test` |
| Hooks | Lefthook | `lefthook install` |

Install: `composer require --dev squizlabs/php_codesniffer wp-coding-standards/wpcs phpstan/phpstan szepeviktor/phpstan-wordpress phpunit/phpunit`.

Fleet/automation repos (many sites managed by scripts): the sensor is a **read-only verification script** run against a staging site after each change (HTTP 200 on key URLs, expected plugin list active, no PHP notices in the log). Put it in the Stop hook; block any command that targets production hosts in `block-dangerous-bash.sh`.

**Lines for `hooks.json`** (2026-09-30): `"format": {".php": "vendor/bin/phpcbf --standard=WordPress {file}"}`, `"lint": {".php": "vendor/bin/phpcs --standard=WordPress {file}"}`, `"stop_test_command": "vendor/bin/phpunit --testsuite unit"` (or the read-only verification script for fleet repos); protected paths to add: `(^|/)wp-config\.php$`, `(^|/)wp-content/uploads/`; deny to add: `wp db reset`, `wp db drop`, `wp site (delete|empty)`, any `ssh` to a production host. Pitfall: `phpcbf` exits non-zero when it fixed something — the guard ignores the format exit code on purpose.
