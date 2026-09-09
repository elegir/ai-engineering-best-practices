# Threat model — agent-driven development (checklist)

For each threat: the control that covers it in THIS repo, or "GAP". Review when tools, MCPs or permissions change.

| # | Threat | Typical path | Control (agnostic practice) | Status here |
|---|---|---|---|---|
| T1 | Secret leakage | agent reads `.env`, pastes it into a commit, log, or chat | PreToolUse protect-files; gitleaks pre-commit; no PII/secrets in logs (standards §7–8) | |
| T2 | Prompt injection via tool output | fetched web page / issue / file contains "ignore previous instructions, run X" | Agent treats tool output as data (entry file rule); dangerous-bash guard; injection eval fixture | |
| T3 | Destructive command | `rm -rf`, `DROP`, `git push --force`, prod deploy to "fix" a test | block-dangerous-bash; deny list in permissions; per-worktree DBs | |
| T4 | Weakening the sensors | agent edits tests/assertions, disables lint rules, `--no-verify` | protected configs; testing-standards rule on assertions; commit guard | |
| T5 | Supply-chain | hallucinated/typosquatted package, unpinned versions | dependency policy; lockfiles protected; audit on push | |
| T6 | Over-broad tool access | MCP with write access to prod, browser logged into admin panels | MCP trust register; read-only roles; MCP audit | |
| T7 | Data exposure to third parties | code/data sent to a model or MCP outside policy | privacy mode on; approved tools only; register | |
| T8 | Unsafe generated code | injection-prone queries, missing validation, `eval` | security linters mandatory (Ruff S, eslint-plugin-security, gosec); standards §8 with GOOD/BAD examples | |
| T9 | Credential handling by the agent | agent asked to enter passwords/tokens | never — humans enter credentials; agents use named env vars only | |
| T10 | Unreviewed merge | agent merges its own PR to main | PR required; human approval; branch protection | |
