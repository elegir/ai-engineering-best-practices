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
| `dot-claude/settings.json` | `<repo>/.claude/settings.json` (merge if exists) | Layer 1: native `permissions.deny` for destructive commands and `.env`/`.claude` edits; wires the guard on PreToolUse, PostToolUse and Stop with `|| exit 2` (fail closed) |
| `dot-claude/hooks/guard.py` | `<repo>/.claude/hooks/guard.py` | Layer 2, one script for all events: protected paths, deny patterns, format + lint after edits, stop gate on the fast tests, `--selftest`. Standard library only; refuses to run while `hooks.json` has a placeholder; any internal error blocks |
| `dot-claude/hooks.json` | `<repo>/.claude/hooks.json` | The only stack-specific input: protected paths, deny patterns, format/lint commands per extension, the stop test command, timeouts |
| `lefthook.yml` | `<repo>/lefthook.yml` | Pre-commit: format check, lint, typecheck, unit; pre-push: integration (the human-side gate; the guard is the agent-side gate) |
| `stack-notes/python.md`, `stack-notes/node.md`, `stack-notes/php-wordpress.md`, `stack-notes/php-laravel.md` | (read) | The exact lines for `hooks.json` per stack, and the stack's pitfalls |
| `dot-claude/hooks/legacy-sh/` | (do not copy) | The four Bash hooks this guard replaced on 2026-09-30; kept for history |

The folder is named `dot-claude/` here because remote tools cannot write `.claude/`; rename it to `.claude/` when copying.

## Reference implementation

`dot-claude/hooks/guard.py` + `dot-claude/hooks.json` + `dot-claude/settings.json`. This is the one place in the KB where the reference **is** the artefact every repo copies regardless of stack (decision 0005 §6): the guard runs around the agent on the developer's machine, not inside the product, so there is nothing to port — only `hooks.json` changes per stack. *Idiom, not required:* nothing; the three files are copied as they are. A repo whose developer machine has no Python at all falls back to `legacy-sh/` and accepts its weaknesses.

## Stack-sensitive points

- The guard runs on the **developer's machine** around the agent, not on the product's host: its runtime is whatever the developer has (Python 3 is assumed; the `|| exit 2` wiring makes its absence block, not pass).
- Test / format / lint commands are the only stack-specific input: `pytest` + `ruff`; `npm test` + `biome`; `vendor/bin/pest` + `pint`/`phpcbf`; WP-CLI checks for WordPress. They live in `hooks.json` (see `variants/*.md` for each stack's lines).
- Protected paths differ: `.env` and lockfiles everywhere; `wp-config.php` on WordPress; `bootstrap/cache/config.php` on Laravel after `config:cache` (secrets are copied there); `*.pem`, `*.key` anywhere.
- Windows: shell hooks need Git Bash; the Python guard removes that dependency, which is the main reason for the rewrite.

## Adapt

1. Copy the three files; rename `dot-claude/` to `.claude/`.
2. In `settings.json` replace `<<PYTHON>>` with the interpreter name that works on **this machine** (`python3` on macOS/Linux/Git Bash; `python` or `py -3` on Windows) — test it in the same shell Claude Code uses — and the two allow-list commands.
3. In `hooks.json` replace every `<<…>>`: the repo-specific protected path (`wp-config.php`, `bootstrap/cache/`, merged migrations), the repo-specific deny (production hosts, `wp db reset`, deploy commands), the format/lint commands per extension (copy the lines from `stack-notes/<stack>.md`; delete extensions the repo has no tool for), the stop test command (fast: under ~60 s), the timeouts.
4. Run `<<PYTHON>> .claude/hooks/guard.py --selftest` until it prints OK: it checks that every tool resolves and that the protected/deny lists cover `.env`, the hooks themselves, `--force`, `--no-verify` and `rm -rf`.
5. Add the self-test line to the entry file's startup routine (`../agent-entry-file/`, assertion 6) so a dead guard is reported every session.
6. Merge `lefthook.yml`; install lefthook (`npm i -D lefthook` / `pip install lefthook` / `composer require --dev` equivalent) and run `lefthook install`.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

1. Asked to edit a protected file (`.env`, lockfiles, the hooks themselves), the agent is blocked before the write and reports the reason — observer: agent — negative: the edit lands
2. After the agent writes a badly formatted file, the file is auto-formatted and any lint error returns to the agent, which fixes it — observer: agent — negative: a file left unformatted, or a lint error the agent never sees
3. With a failing test, asked to "finish", the agent is refused by the stop gate until the test passes — observer: agent — negative: the session ends green with a red test
4. A destructive command from the agent (`--no-verify`, force push, a database drop, a production deploy) is blocked by the guard **and** by the tool's native deny list — observer: agent — negative: either layer alone lets it through
5. The guard fails closed: with the interpreter renamed or missing, every guarded action is blocked and the error names the guard — observer: script — negative: an action that proceeds with "command not found" on stderr (decision 0005 §6)
6. `guard --selftest` passes on a clean tree and is run by the entry-file startup routine — observer: script — negative: a session that starts without the self-test result
7. The pre-commit gate (lefthook or the repo's equivalent) passes on a clean tree and fails on a staged secret or a failing lint — observer: script — negative: a clean tree that fails, or a secret that passes — framework: bends

**Example commands (Python / Node):** `python3 .claude/hooks/guard.py --selftest`; `echo '{"tool_input":{"file_path":".env"}}' | python3 .claude/hooks/guard.py pre-edit; echo $?` → `2`; with the interpreter renamed, any guarded edit → "command not found" **and** blocked (the `|| exit 2`); `npx lefthook run pre-commit`.

## Sources

- Practitioner guide §2 (four hook patterns, JSON `additionalContext`, protected configs, fast Rust tools, feedback-speed table) — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.2.
- Boris Cherny: PostToolUse formatter, `/permissions` pre-allow, Stop hook for long tasks — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2.
- Claude Code hooks docs: https://code.claude.com/docs/en/hooks-guide

## Change log

- 2026-09-30 — the four Bash hooks replaced by `guard.py` + `hooks.json` + a rewired `settings.json` (fail closed with `|| exit 2`, refuses placeholders, `--selftest`, native deny list as layer 1); `variants/` renamed `stack-notes/` and `php-laravel.md` added. Decision 0005 §6; `sources/2026-09-30-stack-debate.md` attack 5.
- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).

- 2026-09-08 — created.
