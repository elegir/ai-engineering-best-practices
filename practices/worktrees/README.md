---
title: "Practice — worktrees (one ticket, one folder, one session)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-30
tags: [worktrees, parallel-agents, isolation, windows]
kind: working-style
applies-when: "parallel_sessions"
when: day-0   # day-0 | first-user | at-scale — when in a product's life this practice is installed (decision 0004 §5)
reference-status: untested   # untested | field-tested | reference (decision 0005 §3)
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

## Reference implementation

`scripts/new-worktree.sh` / `.ps1` and `remove-worktree.sh`, plus `isolation.md`. The scripts assume a per-worktree database and app port; they are a reference for the *steps*, and a repo with Docker Compose profiles or a `.envrc` per folder satisfies the contract differently.

## Stack-sensitive points

- **WordPress stores its URL in the database**, so a worktree with its own port needs its own database *and* a search-replace of the URL — in practice a staging clone, not a worktree; the practice then reduces to "one session per site" (`../hooks-and-guards/variants/php-wordpress.md`).
- **Laravel**: `php artisan serve --port` and a per-worktree `DB_DATABASE` in `.env` make it straightforward; queues and caches need a per-worktree prefix.
- **Node**: port and database as in Python; `node_modules` is installed per worktree (large; consider pnpm's store).

## Adapt

- The scripts derive `APP_PORT` and `DB_NAME` from the worktree folder name; edit the base port and the DB commands for your engine (see `isolation.md`).
- Add the repo's real install and seed commands.
- Put `scripts/new-worktree.*` in the definition of done as the *only* way to start a ticket; add "remove worktree after merge" as the last item.
- Claude Code native: `claude --worktree <name>` creates and enters one; subagents with `isolation: worktree` get their own. The scripts add what Claude Code does not (deps, DB, port).

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

1. Creating a worktree for a ticket yields a sibling folder with the environment file copied, dependencies installed, the app started on its own port and its own seeded database — observer: script — negative: a worktree sharing the main database or port
2. Two sessions in two worktrees running their test suites at the same time both pass with no port or database collision — observer: script — negative: a failure that disappears when run alone
3. The worktree list shows every active ticket, and removing a merged worktree leaves no stale entry, folder or database — observer: script — negative: an orphan database after removal
4. The isolation rules in `isolation.md` are applied to every shared resource the repo has (cache, queue, object store), not only the database — observer: Martin — negative: two worktrees writing the same cache namespace

**Example commands (shell / PowerShell):** `scripts/new-worktree.sh T-003-sso-signup`; `git worktree list`; `scripts/remove-worktree.sh T-003-sso-signup`.

## Sources

- LIDR hub §4 "Git worktrees" (mechanics, the tax, `.worktreeinclude`, `claude --worktree`, `isolation: worktree`) — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.4.

## Change log

- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).

- 2026-09-08 — created.
