---
title: "Practice — hooks and guards (turn rules into mechanisms)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [hooks, claude-code, lefthook, pre-commit, guards, linters]
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

## Adapt

- Open each `.sh` and replace the `<<…>>` commands with the stack's tools from `variants/`.
- In `settings.json`, the `permissions.allow` list must contain only commands you consider safe on your machine; remove anything you do not use.
- Add repo-specific protected paths (migrations that are merged, generated files).
- If the repo already has `.claude/settings.json`, merge the `hooks` and `permissions` keys; do not overwrite.
- Install Lefthook: `npm i -D lefthook && npx lefthook install` (Node) or `pip install lefthook` / a downloaded binary; run `lefthook install` once per clone (put it in `development-guide.md` §2).

## Verify

1. Ask the agent to edit `.env` → the edit is blocked and the agent reports the reason.
2. Ask it to write a badly formatted file → after the write, it is auto-formatted and any lint error comes back to the agent, which fixes it.
3. Break a unit test and ask the agent to "finish" → the Stop hook refuses; the agent fixes the test.
4. `git commit --no-verify` from the agent → blocked by the bash guard. A human running it locally is stopped by review (document it).
5. `npx lefthook run pre-commit` passes on a clean tree.

## Sources

- Practitioner guide §2 (four hook patterns, JSON `additionalContext`, protected configs, fast Rust tools, feedback-speed table) — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.2.
- Boris Cherny: PostToolUse formatter, `/permissions` pre-allow, Stop hook for long tasks — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2.
- Claude Code hooks docs: https://code.claude.com/docs/en/hooks-guide

## Change log

- 2026-09-08 — created.
