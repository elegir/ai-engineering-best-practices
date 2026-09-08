---
title: "Practice — worktrees (one ticket, one folder, one session)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [worktrees, parallel-agents, isolation, windows]
principle: principles/06-parallel-agents-and-worktrees.md
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
supersedes: null
superseded-by: null
---

# Worktrees

## Solves

Two agent sessions in the same folder overwrite each other's files; tests fail for reasons unrelated to the task; the shared dev database and port collide. Symptoms: "my changes disappeared"; migrations applied twice; port 3000 already in use; a session on branch A seeing files from branch B.

## Applies when

- More than one agent session (or a session plus Martin) works on the same repo at the same time.
- Subagents split a large job in parallel.
- You would normally create a branch to avoid conflicts.

## Does not apply when

- Ten-minute fixes done one at a time in the main checkout.
- Repos with no local runtime (pure docs).

## Files in this folder

| File | Copy to | Purpose |
|---|---|---|
| `.worktreeinclude` | `<repo>/.worktreeinclude` | Files copied into every new worktree (`.env`, local configs) — Claude Code honors it; the scripts below honor it too |
| `scripts/new-worktree.ps1` | `<repo>/scripts/` | Windows: create worktree, copy includes, install deps, set port + DB name, seed |
| `scripts/new-worktree.sh` | `<repo>/scripts/` | Same for Git Bash / macOS / Linux |
| `scripts/remove-worktree.sh` | `<repo>/scripts/` | Clean removal: drop the per-worktree DB, `git worktree remove`, `git worktree prune` |
| `isolation.md` | read; adapt into `docs/development-guide.md` §5 | Per-worktree port and database patterns for Postgres/MySQL/SQLite/Docker |

## Adapt

- The scripts derive `APP_PORT` and `DB_NAME` from the worktree folder name; edit the base port and the DB commands for your engine (see `isolation.md`).
- Add the repo's real install and seed commands.
- Put `scripts/new-worktree.*` in the definition of done as the *only* way to start a ticket; add "remove worktree after merge" as the last item.
- Claude Code native: `claude --worktree <name>` creates and enters one; subagents with `isolation: worktree` get their own. The scripts add what Claude Code does not (deps, DB, port).

## Verify

1. `scripts/new-worktree.sh T-003-sso-signup` → a sibling folder exists, `.env` copied, deps installed, app starts on its own port, DB `<<db>>_t_003_sso_signup` exists and is seeded.
2. Two sessions, two worktrees, both running tests simultaneously → both green, no port/DB errors.
3. `git worktree list` shows every active ticket; after merge, `scripts/remove-worktree.sh` leaves no stale entries or databases.

## Sources

- LIDR hub §4 "Git worktrees" (mechanics, the tax, `.worktreeinclude`, `claude --worktree`, `isolation: worktree`) — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.4.

## Change log

- 2026-09-08 — created.
