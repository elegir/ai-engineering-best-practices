---
title: "Practice — hooks and guards (turn rules into mechanisms)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-30
tags: [hooks, claude-code, lefthook, pre-commit, guards, linters]
kind: working-style
applies-when: "always"
reference-status: untested   # untested | field-tested | reference (decision 0005 §3)
principle: principles/02-harness-engineering.md
sources:
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
supersedes: null
superseded-by: null
---

# Hooks and guards

## Solves

Rules live only as sentences in the instruction file, so the agent can skip tests, edit `.env`, silence a linter, or commit with `--no-verify`. Symptoms: "done" with a red suite; formatting failures in CI; rules disabled inline; secrets touched. This practice installs three layers of deterministic enforcement: **Claude Code hooks** (milliseconds, every edit), **pre-commit hooks via Lefthook** (seconds, every commit), and **protected files**.

## Applies when

- The repo has a formatter/linter and a test command (if not, install `verification/` first).
- Claude Code is one of the agents (hooks are Claude Code-specific; the Lefthook layer works for every tool and human).

## Does not apply when

- Pure documentation repos (use only the protected-files gate, if anything).
- Repos where the test suite takes > ~5 minutes: keep the Stop hook to a smoke subset and leave the full suite to CI.

## Files in this folder

| File | Copy to | Purpose |
|---|---|---|
| `dot-claude/settings.json` | `<repo>/.claude/settings.json` (merge if exists) | PreToolUse guard, PostToolUse quality loop, Stop completion gate, safe permissions |
| `dot-claude/hooks/protect-files.sh` | `<repo>/.claude/hooks/` | Blocks edits to `.env*`, lock files, linter/formatter configs, CI config |
| `dot-claude/hooks/post-edit-quality.sh` | `<repo>/.claude/hooks/` | Auto-format then lint the edited file; returns violations as JSON context |
| `dot-claude/hooks/stop-gate.sh` | `<repo>/.claude/hooks/` | Runs the fast test subset before the agent may stop; avoids loops |
| `dot-claude/hooks/block-dangerous-bash.sh` | `<repo>/.claude/hooks/` | Blocks `rm -rf`, `DROP`, `--no-verify`, prod deploy commands |
| `lefthook.yml` | `<repo>/lefthook.yml` | Pre-commit: format check, lint, typecheck, unit; pre-push: integration |
| `variants/node.md`, `variants/python.md`, `variants/php-wordpress.md` | (read) | Exact tool commands per stack to paste into the scripts |

The folder is named `dot-claude/` here because remote tools cannot write `.claude/`; rename it to `.claude/` when copying. Scripts are Bash (Claude Code runs hooks through a shell on Windows too — Git Bash is required; note it in `docs/development-guide.md`).

## Reference implementation

The `dot-claude/hooks/*.sh` scripts are the current reference and are **being replaced** by a single `guard.py` + `hooks.json` (decision 0005 §6; the migration is item 3 of `../../sources/2026-09-30-stack-debate.md` §4). Until then the shell scripts stand with their known weaknesses (sed-parsed JSON; fail-open when the shell is missing). Stack commands (test, format, lint) belong in `hooks.json`, never in the guard itself.

## Stack-sensitive points

- The guard runs on the **developer's machine** around the agent, not on the product's host: its runtime is whatever the developer has (Python 3 is assumed; the `|| exit 2` wiring makes its absence block, not pass).
- Test / format / lint commands are the only stack-specific input: `pytest` + `ruff`; `npm test` + `biome`; `vendor/bin/pest` + `pint`/`phpcbf`; WP-CLI checks for WordPress. They live in `hooks.json` (see `variants/*.md` for each stack's lines).
- Protected paths differ: `.env` and lockfiles everywhere; `wp-config.php` on WordPress; `bootstrap/cache/config.php` on Laravel after `config:cache` (secrets are copied there); `*.pem`, `*.key` anywhere.
- Windows: shell hooks need Git Bash; the Python guard removes that dependency, which is the main reason for the rewrite.

## Adapt

- Open each `.sh` and replace the `<<…>>` commands with the stack's tools from `variants/`.
- In `settings.json`, the `permissions.allow` list must contain only commands you consider safe on your machine; remove anything you do not use.
- Add repo-specific protected paths (migrations that are merged, generated files).
- If the repo already has `.claude/settings.json`, merge the `hooks` and `permissions` keys; do not overwrite.
- Install Lefthook: `npm i -D lefthook && npx lefthook install` (Node) or `pip install lefthook` / a downloaded binary; run `lefthook install` once per clone (put it in `development-guide.md` §2).

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

1. Asked to edit a protected file (`.env`, lockfiles, the hooks themselves), the agent is blocked before the write and reports the reason — observer: agent — negative: the edit lands
2. After the agent writes a badly formatted file, the file is auto-formatted and any lint error returns to the agent, which fixes it — observer: agent — negative: a file left unformatted, or a lint error the agent never sees
3. With a failing test, asked to "finish", the agent is refused by the stop gate until the test passes — observer: agent — negative: the session ends green with a red test
4. A destructive command from the agent (`--no-verify`, force push, a database drop, a production deploy) is blocked by the guard **and** by the tool's native deny list — observer: agent — negative: either layer alone lets it through
5. The guard fails closed: with the interpreter renamed or missing, every guarded action is blocked and the error names the guard — observer: script — negative: an action that proceeds with "command not found" on stderr (decision 0005 §6)
6. `guard --selftest` passes on a clean tree and is run by the entry-file startup routine — observer: script — negative: a session that starts without the self-test result
7. The pre-commit gate (lefthook or the repo's equivalent) passes on a clean tree and fails on a staged secret or a failing lint — observer: script — negative: a clean tree that fails, or a secret that passes — framework: bends

**Example commands (Python / Node):** `python3 .claude/hooks/guard.py --selftest`; `mv $(which python3) /tmp && <any guarded edit>` → blocked; `npx lefthook run pre-commit`.

## Sources

- Practitioner guide §2 (four hook patterns, JSON `additionalContext`, protected configs, fast Rust tools, feedback-speed table) — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.2.
- Boris Cherny: PostToolUse formatter, `/permissions` pre-allow, Stop hook for long tasks — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2.
- Claude Code hooks docs: https://code.claude.com/docs/en/hooks-guide

## Change log

- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).

- 2026-09-08 — created.
