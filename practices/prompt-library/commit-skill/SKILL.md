---
name: commit
description: Create a commit in this repository the way the team does it — audit, verify, conventional message with task id, never bypass hooks. Use when asked to commit, save work, or finish a task.
---

# Commit

1. Run the audit (`/audit` or `code-audit.md`). If the verdict is FIX FIRST, fix, then restart this skill.
2. Stage only files belonging to the current task (`git add <paths>`; never `git add -A` blindly). Confirm no `.env*`, lock files, or generated artifacts are staged unless intended.
3. Message format: `type(scope): imperative summary ≤ 72 chars (T-NNN)` with body lines: what changed, why, how verified (commands + results). Types: feat, fix, docs, chore, refactor, test, perf, build, ci.
4. `git commit` — hooks must run; `--no-verify` is forbidden. If a hook fails, fix the cause.
5. Update `PROGRESS.json` (`sessions[].commits`) with the hash.
6. Report: hash, message, files.
