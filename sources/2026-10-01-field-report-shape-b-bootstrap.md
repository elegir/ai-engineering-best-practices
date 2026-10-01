---
title: "Field report — bootstrap of a blank shape-B repo (newsflow: RSS → LLM → WordPress, Python 3.11, cron, SQLite) from the KB's blank-repo door: 8 practices, 13 minutes, ~268k tokens, 22 findings"
type: source
status: current
date: 2026-10-01
tags: [field-report, bootstrap, acceptance-test, shape-b, verification, context-docs-skeleton, agent-entry-file, hooks-and-guards, security-baseline, prompt-library, spec-driven, llm-api-calls, python]
sources:
  - playbooks/bootstrap-new-repo.md
  - practices/bundles.md
  - decisions/0004-day-one-for-blank-and-existing-repos.md
supersedes: null
superseded-by: null
---

# Field report — shape B bootstrap (acceptance test, decision 0004 §8, first arm)

## 1. What was adopted

- **Practices** (all at `last-reviewed: 2026-09-30`): `verification`, `context-docs-skeleton`, `agent-entry-file`, `hooks-and-guards`, `security-baseline` (core + full), `prompt-library`, `spec-driven`, `llm-api-calls` — exactly what `python3 scripts/applies.py --explain llm_calls:planned acts_on_world:planned` printed (= the shape-B blank-repo bundle). Deferred: `token-savings`. Skipped with the script's reasons: `session-state`, `worktrees` (both asked facts "no"), `context-management`, `llm-gateway` (`production` not planned yet), `agent-patterns`.
- **Repo and commits:** sandbox repo `shape-b-pipeline` (a sibling of the KB), `34f3c26` (placeholder README) → `249bbec` ("chore(harness): bootstrap from AI-engineering KB (8f33b0d)"), 55 files, 2,037 lines. KB at `8f33b0d`, untouched.
- **Stack and runtime:** the shape-B default — Python scripts + cron + SQLite + WordPress REST. Machine: Python 3.11.15 (the KB said 3.12), ruff, pytest. Not installed and not installable in the sandbox: gitleaks, lefthook, hurl, pip-audit, the `anthropic` SDK, `feedparser` (declared in `pyproject.toml`; `pip install -e .[dev]` recorded as Martin's first step).
- **Door:** blank repo, facts planned from Martin's paragraph ("lee feeds RSS, reescribe con un modelo, publica solo por cron en mis WordPress; nunca publicar sin validar, nunca dos veces") and the three intent questions (payments: no; several companies: no; acts alone: yes) plus the two workflow questions (no, no). Facts block in the repo's `AGENTS.md`, thirteen lines, each `planned 2026-10-01` or `asked 2026-10-01`; `production: no — planned` (becomes yes at the first approved live run); `personal_data: no — planned` (public news text; a judgment call, see §5.17).
- **Who ran it:** a clean-context agent (Claude, Claude Code subagent) with Martin's answers supplied in advance; 14:32–14:45 UTC; one session; 69 tool calls.

## 2. The contract — assertion by assertion (condensed; the full table is in the session transcript)

| Practice | Assertions | Outcome |
|---|---|---|
| `verification` | 1 smoke in one command (8 tests, 0.09 s) · 2 broken flow fails readably and the stop gate blocks · 3–5 handed to Martin / trivially true · 6 dry-run switch `PUBLISH_MODE`, payload asserted, effect absent, live refused outside production, first run capped to 1 post | 1, 2, 6 pass with negatives performed; 3, 4 handed to Martin; `dry-run-and-approval.md` 1–3 pass, 4 n.a. (never run live) |
| `context-docs-skeleton` | 4 index = files (passed after one fix) · 5 no placeholders | 4, 5 pass; 1–3 need a fresh interactive session (handed to Martin) |
| `agent-entry-file` | 1 fifty lines · 4 every prohibition names its enforcer · 5 facts block · 6 self-test in the startup routine | 1, 4, 5, 6 pass; 2, 3 handed to Martin |
| `hooks-and-guards` | 1 `.env` and repo-specific files blocked · 2 post-edit formats and returns `F821` · 3 stop gate blocks once, lets the second attempt through · 4 `--no-verify`, `rm *.sqlite3`, `PUBLISH_MODE=live` blocked · 5 fail-closed with a missing interpreter and with a placeholder left · 6 self-test OK | 1–6 pass (script level, negatives performed); 7 n.a. — lefthook and gitleaks not installed (the `.env` refusal snippet verified by hand) |
| `security-baseline` | core 2 pass (by hand), 1 and 3 n.a. (tools missing), 4 handed; full 6, 7 handed (register and threat model T1–T11 filled, three `GAP (Martin)`), 5 n.a. (fixture is first-user), 8 n.a. (one route, no tenants), 9 pass by code review | no failure; three n.a. for missing tools |
| `prompt-library` | 5 installed as seven commands + one skill | 5 pass; 1–4 handed to Martin |
| `spec-driven` | 4 constitution (11 rules, rule 11 = Martin's two "nunca") | 4 pass (vacuously); 1–3 handed |
| `llm-api-calls` | 1 one module imports the SDK · 2 versioned prompt with header · 4 one retry owner, attempt logged (added — the skeleton did not log it) · 6 usage logged · 9 provider doc dated with switching cost | 1, 2, 4, 6, 9 pass; 3 n.a. (≈415 static tokens, under the cacheable minimum; no SDK here); 5, 7 handed; **8 fail/pending** — no eval exists yet (`last-evaluated: never`) |

## 3. Stack-sensitive points applied

SQLite in memory instead of the Postgres/testcontainers fixture; one switch `PUBLISH_MODE` (the KB's own files disagreed on its name — fixed, see §5.3); `.claude/` excluded from ruff because the verbatim `guard.py` was not format-clean (fixed in the KB the same day); `pip-audit` has no severity threshold → policy says any finding blocks; `stack-notes/python.md` for `llm-api-calls` existed and was followed (official SDK, `max_retries=0`, explicit `cache_control`, usage log). Every template assumed `PROGRESS.json`; with `session-state` skipped, the references were pointed at the open spec.

## 4. Cost (mandatory)

| Measure | Value |
|---|---|
| Tokens spent (whole session, harness counter) | **268,069** |
| Wall-clock minutes | **13** (14:32:02 → 14:44:54 UTC) |
| Wrong API / framework calls caught by Verify | **3** — pytest ran under a tool interpreter without `httpx` (caught by assertion 1; lazy import); ruff `S106` flagged a variable named `token_env` as a hard-coded password (renamed); the docs-index check caught a backticked name of a deleted document. Zero wrong vendor-API calls — the Anthropic path could not execute (SDK absent) |
| Of those, how many the stack-notes would have prevented | 0 |

Decision 0005 §8's threshold (100,000 tokens per practice for *translation*) does not apply: this was a Python bootstrap of eight practices, ≈ 33k tokens per practice including the walking skeleton.

## 5. What the KB should change (verdicts in impact-table vocabulary; **all applied 2026-10-01** unless marked park)

1. **contradicts** — `stack-defaults.md` shape B listed only the core security files while the router printed `security-baseline (full)` for `acts_on_world:planned`. → Shape B lists the full part.
2. **contradicts** — the bootstrap's commit message failed the Conventional Commits regex the bootstrap itself installs. → `chore(harness): …`.
3. **contradicts** — the dry-run switch had three names in one practice (`DRY_RUN=1`, `SEND_MODE`, the `DRY_RUN_VAR` placeholder). → one placeholder, example `PUBLISH_MODE`, in all three files.
4. **contradicts** — `guard.py` was not `ruff format`-clean, so the bootstrap's own `format-check` would reject the first commit. → formatted.
5. **refines** — `bootstrap-new-repo.md` did not say that a *walking skeleton* is part of day zero although `verification` 1, 2 and 6 need code to run. → stated in step 5.
6. **refines** — "production is no until there is a user" contradicted `facts.md` for a system that never has users. → "until the first approved live run".
7. **refines** — asked facts: say that an absent fact is "no". → stated. (`applies.py --help` prints the empty-facts list instead of usage — park, cosmetic.)
8. **new** — every template assumes `PROGRESS.json`; when `session-state` is skipped there was no fallback. → "point them at the open spec" in the bootstrap.
9. **new** — `llm-api-calls` assertion 4 requires the retry count in the log; the skeleton did not log it. → `attempt=%d` added.
10. **contradicts** — the README's example `python3 llm_call_skeleton.py --demo` did not exist. → `--demo` added (prints the request shape without calling); note that the file parses only after its three placeholders are replaced.
11. **refines** — caching assertion is n.a. for a one-prompt rewrite on day zero. → said in shape B.
12. **new** — `implement-practice.md` lacked command frontmatter and carried a KB-facing preamble. → frontmatter + `$ARGUMENTS`; explanation moved to the README row.
13. **refines** — `harness-evals.md` E1 named `/start-session`, which no day-zero practice installs. → reworded.
14. **refines** — the injection fixture was "full part" in the README and "first-user" in shape A. → marked first-user in the README's Files table.
15. **refines** — `hooks.json` kept a literal placeholder token in its comment, tripping every `grep '<<'` check. → reworded.
16. **refines** — the native deny layer is narrower than `hooks.json` (no regex); say so. → said in the Files table.
17. **park → applied as a clarification** — `personal_data` for public text about people. → `facts.md` row clarified (public text about people ≠ personal data; contact/account/conversation data = yes).
18. **refines** — Python 3.12 vs the machine's 3.11. → "or the machine's 3.11+, record it".
19. **refines** — `docs/stack.md` is asked for in step 4 but exists after step 5. → "record it when `docs/` is copied".
20. **refines** — `verification` assertion 2's stop-gate half depends on `hooks-and-guards`, installed later. → re-check noted in step 5.
21. **confirms** — `applies.py --explain` = the shape-B bundle exactly; `guard.py` self-test, fail-closed and placeholder refusal behave as documented; `kb-sync.sh` in sync.
22. **park** — assertions with observer `agent` (context-docs 1–3, entry-file 2–3, prompt-library 1–2, spec-driven 1–2) cannot be judged from a scripted bootstrap; they are the first harness-eval run in Martin's next interactive session on this repo.

## 6. Files produced in the repo (`shape-b-pipeline@249bbec`)

`AGENTS.md` (50 lines, with the facts block), `CLAUDE.md`, `.claude/settings.json`, `.claude/hooks.json`, `.claude/hooks/guard.py` (verbatim), seven commands and one skill under `.claude/`, `lefthook.yml`, `pyproject.toml`, `.env.example`, `docs/` (sixteen documents including `dry-run-and-approval.md`, `threat-model.md`, `mcp-trust-register.md`, `llm-provider.md`, `harness-changelog.md`), `specs/constitution.md`, `prompts/rewrite/system.md` (versioned, static-first), `src/newsflow/` (config with the one switch, SQLite dedupe store, validator, publisher with injectable transport, pipeline, `llm.py` from the skeleton, feeds, CLI) and `tests/` (seeded store, fake rewriter, counting transport, eight smoke tests). Candidate variant: none — this is the reference stack; the repo is the first evidence that the Python reference files work.

## 7. Verdict for decision 0004 §8

The blank-repo door works end to end in the reference stack: thirteen minutes from an empty repo to a committed harness with a passing smoke suite, a fail-closed guard and a facts block, with no question that needed Martin beyond the five the playbook asks. The valuable output was the twenty-two findings, nineteen of them fixed the same day. Open: the `agent`-observer assertions need one interactive session; `llm-api-calls` has no eval yet (assertion 8); three tools (gitleaks, lefthook, pip-audit) could not be installed in the sandbox, so the pre-commit gate is unverified. Shape A is the second arm.
