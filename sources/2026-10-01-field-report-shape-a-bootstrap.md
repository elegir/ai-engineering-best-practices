---
title: "Field report — bootstrap of a blank shape-A repo (outreachhub: multi-tenant cold-email SaaS exposing MCP tools, Python 3.11, SQLite in the sandbox) from the KB's blank-repo door: 13 practices, 23 minutes, ~297k tokens, 26 findings"
type: source
status: current
date: 2026-10-01
tags: [field-report, bootstrap, acceptance-test, shape-a, verification, context-docs-skeleton, agent-entry-file, hooks-and-guards, security-baseline, session-state, prompt-library, spec-driven, worktrees, llm-api-calls, agent-patterns, python]
sources:
  - playbooks/bootstrap-new-repo.md
  - practices/bundles.md
  - decisions/0004-day-one-for-blank-and-existing-repos.md
  - sources/2026-10-01-field-report-shape-b-bootstrap.md
supersedes: null
superseded-by: null
---

# Field report — shape A bootstrap (acceptance test, decision 0004 §8, second arm)

## 1. What was adopted

- **Practices**, in the router's order, all at `last-reviewed: 2026-09-30`: `verification`, `context-docs-skeleton`, `agent-entry-file`, `hooks-and-guards` (already field-tested that morning), `security-baseline` core + full, `session-state`, `prompt-library`, `spec-driven`, `worktrees`, `llm-api-calls`, `agent-patterns` — thirteen entries counting the security full part; `token-savings` deferred (first-user); `context-management` and `llm-gateway` skipped by the script (no `multi_turn`/`retrieval`; `production` not planned). `python3 scripts/applies.py --explain llm_calls:planned exposes_tools:planned acts_on_world:planned multi_tenant:planned personal_data:planned regulated:planned parallel_sessions long_tasks` = bundle A (blank) plus `session-state` and `worktrees` because both asked facts were yes.
- **Repo and commits:** sandbox repo `shape-a-saas`, `359e05e` (placeholder README) → `39bb484`, one commit, 60 files; branch renamed `master` → `main`. KB at `412086c`, untouched.
- **Stack and runtime:** shape-A default accepted with recorded deviations (`docs/stack.md`): Python 3.11.15; SQLite instead of PostgreSQL + RLS (nothing installable in the sandbox); no FastAPI → the walking skeleton is a CLI package and the API is task T-003; lefthook, gitleaks, pip-audit, hurl absent → stop-gap gates in `lefthook.yml` and task T-008. The `anthropic` SDK was present; no network call was made.
- **Door:** blank repo. Martin's paragraph: a SaaS for small law firms to run cold-email prospecting — each firm its own space (contacts, templates, mailboxes); sequences sent on a schedule; results written to the firm's CRM; functions exposed as MCP tools to an external agent (Claude Desktop); the product itself uses a model to draft and classify replies; never email someone who opted out; one firm's data never visible from another. Intent answers: payments yes (Stripe; CAN-SPAM; data protection), several companies yes, acts alone yes; both workflow questions yes. Facts block: fourteen lines in `AGENTS.md`, each with Martin's sentence; `tools: no` (the deciding model lives outside), `exposes_tools: yes`, `production: no — planned`. Four questions left for Martin in `PROGRESS.json` (suppression scope, email transport, first CRM, queue engine).
- **Who ran it:** a clean-context agent, 14:51–15:15 UTC, 88 tool calls.

## 2. The contract — condensed (full tables in the transcript)

| Practice | Outcome |
|---|---|
| `verification` | 1 (8 tests, 0.4 s), 2 (suppression removed → two named failures; stop gate blocks; re-checked after the guard), 6 (`SEND_MODE`; live refused outside production with one line and exit 2; dry run logs the payload and calls no transport; cap 10; negative performed) pass; 3–5 handed to Martin |
| `context-docs-skeleton` | 4, 5 pass with negatives observed mid-run; 1–3 need an interactive session |
| `agent-entry-file` | 1 (49 lines), 5, 6 pass; 2–4 handed |
| `hooks-and-guards` | 1–6 pass with negatives (`--force-with-lease` allowed, `--force` blocked); 7 partial — lefthook not installable, each gate run by hand (secret, `.env`, commit-msg) |
| `security-baseline` | core 1–2 pass by hand with a grep stop-gap for secrets; 3 n.a. (pip-audit missing); 4, 6, 8 handed; 7 pass (13 rows, no empty status); 5 n.a. (first-user); 9 pass, with a finding: the mailer logs the recipient address at INFO |
| `session-state` | 3, 4 pass (commit names the task in the body; `PROGRESS.json` valid with `updated` per task); 1–2 need a live session. **The KB template fails its own assertion 4** (no date field) — fixed |
| `prompt-library` | 5 pass (nine commands, one skill, four paste prompts under `prompts/library/`); 1–4 handed |
| `spec-driven` | 4 pass (constitution, 14 rules; spec 0001 references it); 1–3 handed |
| `worktrees` | 1–3 pass **after two fixes to the KB script** (default base branch `main` failed on `master`; the include loop died under `set -e`); 4 handed |
| `llm-api-calls` | 1, 2, 4 (attempt in the log), 6 (`--demo`), 7, 9 pass; 3 n.a. (short prefixes); 5 handed; 8 n.a. — no eval yet (task T-005 requires 5× and worst case) |
| `agent-patterns` | 1 pass (spec records workflow + exposed tools, no loop); 3 handed (template placed as `docs/tool-definition-template.md`); 2, 4, 5 n.a.; 6 ongoing |

## 3. Stack-sensitive points applied

SQLite file per worktree (`isolation.md`) — but the app had no `.env` loader, so the override was silent until a ten-line dotenv reader was added; `test_cli_entrypoint_help` failed on the src layout (`PYTHONPATH` does not reach subprocesses); the copied `guard.py` failed the repo's `ruff format --check` at line length 110 (excluded `.claude/`); `max_retries=0`, retry owner the module; `SEND_MODE=live` and `APP_ENV=production` added to the deny list. Missing when needed: `verification/stack-notes/python.md` and `security-baseline/stack-notes/python.md` (written the same day).

## 4. Cost (mandatory)

| Measure | Value |
|---|---|
| Tokens (harness counter) | **297,335** |
| Wall-clock minutes | **23** (14:51:36 → 15:14:51 UTC) |
| Wrong API / framework calls caught by Verify | **5**: CLI test on src layout; format check on the copied guard; worktree script `main` vs `master`; worktree include loop under `set -e`; a module-level `settings = load()` turning the one-line refusal into a traceback. Plus one lint catch (`typing.Callable` → `collections.abc`) |
| Of those, how many the stack-notes would have prevented | **2** (now in `verification/stack-notes/python.md` and the hooks README §Adapt); two were script bugs (fixed in the KB); one is a product rule now in the Python notes |

Per practice ≈ 23k tokens; below the 100k-per-practice threshold of decision 0005 §8 by a wide margin, in the reference stack.

## 5. What the KB should change (verdicts; **all applied 2026-10-01** unless marked park)

1. **contradicts** — `applies.py` listed `token-savings [first-user]` for a blank repo when the two asked facts were passed, because "blank" was computed as "no inferred facts" and asked facts counted. → asked facts no longer count as code evidence; the practice is deferred.
2. **new** — step 0 `--pull` in a read-only session. → stated as allowed.
3. **refines** — the bootstrap commit shape left no room for `(T-NNN)` in the head line, which `session-state` assertion 3 wanted. → assertion accepts head line or body.
4. **contradicts** — `PROGRESS.json` template had no per-task date although assertion 4 requires one. → `updated` added to every task and to the rules line.
5. **new** — `new-worktree.sh` defaulted to `main` and fetched a non-existent `origin`. → default is the current branch; fetch only if a remote exists.
6. **new** — the `.worktreeinclude` loop's `&&` chain exits the script under `set -e` when the last include is missing. → `if`.
7. **new** — `isolation.md` assumed the app reads `.env`. → section added.
8. **new** — `test_cli_entrypoint_help` fails on a src layout. → `PYTHONPATH=src` passed to the subprocess.
9. **new** — no `verification/stack-notes/python.md` for the reference stack. → written (walking skeleton, src layout, seeding, one-line refusal, pytest interpreter pitfall).
10. **refines** — "formatted with ruff" holds only at the default line length. → §Adapt step: exclude `.claude/` from the repo's formatter.
11. **new** — `hooks.json` deny example lacked the dry-run switch. → `SEND_MODE=live` first in the example.
12. **refines** — `no-env-files` also refused `.env.example`. → excluded.
13. **new** — no `security-baseline/stack-notes/python.md`. → written (gitleaks, pip-audit, Ruff S, stop-gaps, logging rule, n.a. rule).
14. **park → decided** — "tool not installable" as n.a.: accepted only with that reason and an open task; stated in the Python security notes.
15. **refines** — `implement-practice.md` line 5 still had the PRACTICE placeholder. → `$ARGUMENTS`.
16. **refines** — per-use placeholders in paste prompts collide with the repo-wide placeholder scan. → rule in the prompt-library README (`prompts/library/` with its README, excluded from the scan).
17. **new** — where the tool-definition template goes before any tool exists. → `docs/tool-definition-template.md` on day zero.
18. **refines** — shape A named no queue engine. → default: a `jobs` table in the same database until volume demands a broker.
19. **refines** — shape A listed `api-hurl/` on day zero with no HTTP surface. → "with the first endpoint".
20. **new** — no rule for an uninstallable default stack. → step 4: record as planned, build with what runs.
21. **refines** — context-docs assertion 4 vs template index entries for files that do not exist yet. → "every existing file; planned entries marked".
22. **confirms** — walking-skeleton rule (5a) and the stop-gate re-check (5b) from the shape-B report were necessary and worked.
23. **confirms** — `hooks-and-guards` behaved exactly as documented, second repo in a row.
24. **new** — the field-report template is written for one practice. → bootstrap note added to §1.
25. **park** — a dated "known model ids" line in the Python stack-notes vs an env-driven default; left as the env override the agent chose; revisit when the first real call is made.
26. **park** — the facts block takes a third of the entry file's sixty-line budget; assertion 5 already allows a pointed-to file; no change.

## 6. Files produced (`shape-a-saas@39bb484`)

`AGENTS.md` (49 lines, 14 planned facts), `CLAUDE.md`, `.claude/` (settings with the native deny list and the guard wired `|| exit 2`, `hooks.json` with eleven protected and thirteen deny patterns including `SEND_MODE=live`, prod ssh/deploy and the Stripe charge command, `guard.py` verbatim, nine commands, the commit skill), `lefthook.yml` with stop-gap gates, `pyproject.toml`, `src/outreachhub/` (`config.py` with `SEND_MODE`/`APP_ENV`/`FIRST_RUN_CAP` and a dotenv reader; `db.py` where every function takes `tenant_id` and suppression is enforced in SQL; `mailer.py` with an injectable transport and an outbox; `pipeline.py`; CLI with `health` and `send`; `llm.py` from the skeleton), `tests/` (seeded SQLite with two tenants and one opted-out contact; eight smoke tests including tenant isolation and suppression), sixteen `docs/` files (threat model with thirteen rows, trust register with four planned product tools and their blast radius, provider decision, tool-definition template), `specs/constitution.md` (14 rules) and `specs/0001-walking-skeleton.md`, `PROGRESS.json` (eight tasks, four questions), two versioned prompts (`classify-reply`, `draft-email`) with an injection rule, worktree scripts with the two fixes. Candidate variant: none (reference stack).

## 7. Verdict for decision 0004 §8

Both arms of the acceptance test passed in the reference stack: 13 and 23 minutes, 268k and 297k tokens, no question needed beyond the five the playbook asks, and the heavy shape produced tenant isolation and suppression as tested code on day zero. The two runs found 48 defects in the KB, 44 fixed the same day; the second run found none of the first run's defects again, which is the sign the fixes held. Open: the `Martin`- and `agent`-observer assertions (one interactive session per repo), the LLM evals (assertion 8 in both repos), and the gates that need gitleaks/lefthook/pip-audit installed. The Laravel two-arm experiment (decision 0005 §10) is the next evidence step.
