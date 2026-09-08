---
title: "Parallel agents and git worktrees — isolate, don't coordinate"
type: principle
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [worktrees, parallel-agents, subagents, isolation]
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Parallel agents and git worktrees

## 1. The question this answers

How do you run several agent sessions (or subagents) on the same repository at the same time without them overwriting each other, corrupting the dev database, or failing tests for unrelated reasons?

## 2. Short answer

Give each session its own **git worktree** — a separate folder on disk with its own branch, sharing the repo's history — and, for full isolation, its own database and dev-server port. The fix is *physical isolation at the filesystem level*, not clever coordination between agents. Use `claude --worktree <name>` for sessions and `isolation: worktree` for subagents. Accept the "worktree tax" (reinstall dependencies, copy `.env` via `.worktreeinclude`) and skip worktrees for ten-minute tasks. Get one agent working reliably before scaling to many.

## 3. Long explanation

### The problem

A normal checkout has one active branch. If an agent is mid-feature on `feature/payments`, the folder is in that intermediate state; a second session on the same folder overwrites changes, tests fail for reasons unrelated to either feature, and the dev database ends up inconsistent.

### The mechanism

```bash
git worktree add ../my-project-payments feature/payments   # create a sibling folder on that branch
git worktree list
git worktree remove ../my-project-payments                 # when merged
claude --worktree feature-name   # Claude Code: creates the worktree, opens the session inside, asks keep/delete on exit
```

Each agent sees only its own files and is unaware other sessions exist. Subagents can be isolated the same way (`isolation: worktree`) — essential when one agent splits a large job across parallel subagents. Superpowers uses worktrees natively and can merge the worktree back automatically.

### The tax

- Each worktree is a fresh checkout: no `.env`, no `node_modules`/venv. Reinstall, or list what to copy in a `.worktreeinclude` file.
- Files are isolated; **infrastructure is not**. Two worktrees sharing a database or a dev port still collide. For complete isolation combine with per-branch databases (or schemas) and per-session ports.
- Setup cost is real. Rule: *if you would normally create a branch to avoid conflicts, use a worktree; otherwise don't.*

### How the pros run in parallel

Boris Cherny runs ~5 local Claude Code sessions in numbered terminal tabs with system notifications, plus 5–10 cloud sessions, hands local sessions to the web (`&`, `--teleport`), and starts sessions from his phone. Vercel/LIDR both stress: fewer, isolated, well-harnessed agents beat many uncoordinated ones. The practitioner guide's warning: scaling agent count without a harness produces "compounding cognitive debt, not leverage" — polish with one agent, then scale.

### Martin's current state

`Local Coding/` already contains many `wt-*` folders (`wt-copy-guards`, `wt-multiflow`, `wt-serp-validator`, …) — worktrees are in use. The likely gaps are the tax items: `.worktreeinclude`, per-worktree DB/port isolation, and a cleanup routine (`git worktree prune`; delete merged worktrees).

## 4. How to apply it in a repo

1. Add `.worktreeinclude` listing `.env*` and any local config the agent needs.
2. Document in `docs/development-guide.md` how to start the stack on an alternate port and against an alternate DB name/schema, parameterized by worktree name.
3. Standardize: one ticket = one worktree = one session. Name worktrees after the ticket.
4. Add a `/new-worktree` command or skill that creates the worktree, installs deps, copies includes, and points the DB.
5. Add cleanup to the definition of done: merged → `git worktree remove`.
6. Keep the main checkout for review and merges only.

## 5. Anti-patterns

- Two agents in one folder.
- Worktrees sharing a database while both run migrations.
- Forgetting to prune; dozens of stale worktrees and branches.
- Parallelizing before a single-agent task completes reliably end to end.

## 6. Evidence & sources

- LIDR hub §4 "Git Worktrees" — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.4.
- Cherny's parallel setup — same file §3.2.
- Practitioner guide anti-pattern "scaling without a harness" — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.2.

## 7. Change log

- 2026-09-08 — created.
