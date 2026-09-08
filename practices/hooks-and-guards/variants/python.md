# Variant — Python

| Purpose | Tool | Command |
|---|---|---|
| Format | Ruff | `ruff format <file>` |
| Lint | Ruff (replaces flake8, isort, pyupgrade, Black) | `ruff check <file>` (use `--fix` in PostToolUse for auto-fixable rules) |
| Security lint | Ruff `S` rules (bandit) | enable `select = ["E","F","I","UP","B","S"]` in `pyproject.toml` |
| Architecture boundaries | ast-grep or import-linter | `lint-imports` |
| Types | mypy or pyright | `mypy .` |
| Unit | pytest | `pytest -q -x tests/unit` |
| Integration | pytest + testcontainers | `pytest -q tests/integration` |
| API e2e | Hurl or pytest + httpx | `hurl --test tests/api/*.hurl` |
| Hooks | Lefthook (binary) or pre-commit | `pip install lefthook && lefthook install` |

Pipelines/cron-style repos (ETL, scrapers, email senders): the "e2e" is a dry-run against a seeded DB with `--limit 5` and assertions on the resulting rows; put that command in the Stop hook.
