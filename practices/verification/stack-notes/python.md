# Stack-notes — Python (the reference stack)

Written 2026-10-01 after the two bootstraps (shapes A and B). Check current versions at adoption.

- **Walking skeleton for day zero** (playbook step 5a): `src/<app>/config.py` (the one dry-run switch, `live` refused outside production), `src/<app>/<effect>.py` (the single side-effecting module with an injectable transport), a `pipeline.py`/`__main__.py` entry point, and `tests/conftest.py` seeding SQLite in memory. That is what `python-pytest/` tests; nothing else is needed for assertions 1, 2 and 6.
- **src layout:** pytest's `pythonpath = ["src"]` (pyproject) does not reach subprocesses — the CLI test passes `PYTHONPATH=src` (already in `test_smoke.py`) or the repo runs `pip install -e .`.
- **Seeding:** SQLite in memory or a file per test session; Postgres with testcontainers only once Docker is available on the machine.
- **Dry-run switch:** an environment variable read once in `config.py` (`PUBLISH_MODE` / `SEND_MODE`); tests set it through `monkeypatch`; the same name goes into `hooks.json` → `deny_commands` as `<NAME>=live`.
- **One-line refusal:** keep settings loading lazy or wrap it — a module-level `settings = load()` turns the "refuse `live` outside production" rule into a traceback at import instead of one line and exit 2.
- **Smoke command:** `pytest -q -x tests/test_smoke.py`; the full suite stays in CI.
- **Pitfall:** a uv/pipx-installed pytest runs under its own interpreter and does not see the project's dependencies; use `python3 -m pytest` from the project environment.
