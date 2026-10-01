# Stack-notes — Python (the reference stack)

Written 2026-10-01 after the two bootstraps. Check current versions at adoption.

- **Secret scan:** gitleaks (`brew install gitleaks` / `winget install gitleaks` / release binary); until it is installed, a stop-gap pre-commit grep for `AKIA[0-9A-Z]{16}`, `sk-ant-`, `sk-`, `ghp_`, `-----BEGIN .*PRIVATE KEY` on the staged diff — and task T-xxx to install the real tool. Record the stop-gap in `docs/harness-changelog.md`.
- **Dependency audit:** `pip-audit` (`pip install pip-audit`), fails on any known vulnerability; `--ignore-vuln` per advisory with a reason in the policy log. Until installed: the policy says "manual check of PyPI advisories on every new dependency".
- **Security lint:** Ruff `S` rules (`select = ["E","F","I","UP","B","S"]`); `S106`/`S105` flag any variable or argument named like a secret — name the *environment-variable name* holder `credential_env`, not `token`.
- **Secrets at runtime:** read once in `config.py` from the environment; `.env` never committed (`.env.example` is); the guard protects `.env*` and `config.py`.
- **Logging:** never log request headers or full payloads from the side-effecting module; in `acts_on_world` repos the recipient address at INFO is personal data — log an id or a hash.
- **n.a. rule:** "tool not installable on this machine" is an acceptable `n.a.` for assertions 1 and 3 only with that exact reason and an open task; in a real repo the tools install in minutes and the assertions are expected to pass.
