---
title: "Practice — session state (progress file + startup routine)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [state, progress, session, resumability]
kind: working-style
applies-when: "long_tasks or parallel_sessions"
principle: principles/02-harness-engineering.md
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Session state

## Solves

Every agent session starts with an empty memory. Long tasks lose their place when the context compacts, the session ends, or the machine reboots; a second agent (or the same one tomorrow) redoes finished work or continues from the wrong step; questions asked to Martin get lost. Symptoms: "let me first understand the codebase" at the start of every session; duplicated work across worktrees; half-finished tasks with no trace of what remains.

## Applies when

- Any task longer than one session, any repo touched by several sessions or agents, any repo with worktrees.

## Does not apply when

- One-shot scripts. (Even then, a `git log` discipline is enough.)

## Files in this folder

| File | Copy to | Purpose |
|---|---|---|
| `PROGRESS.json` | `<repo>/PROGRESS.json` | Machine-friendly task list and session log (JSON: models are less likely to mangle it than Markdown) |
| `dot-claude/commands/start-session.md` | `<repo>/.claude/commands/start-session.md` | `/start-session`: the standardized startup routine |
| `dot-claude/commands/end-session.md` | `<repo>/.claude/commands/end-session.md` | `/end-session`: update progress, commit, summarize |
| `startup-routine.md` | paste into `AGENTS.md` "Start of every session" | The three-line routine for tools without commands |

## Adapt

- Fill the `health_check` and test commands in `PROGRESS.json.meta`.
- If the repo uses an SDD tool (OpenSpec), tasks in `PROGRESS.json` reference the change/spec id rather than duplicating its task list.
- Decide who may edit `PROGRESS.json`: agents append to `sessions` and flip task `status`; humans edit `tasks`. Say so in `AGENTS.md`.
- Keep the file small: archive `sessions` older than 30 days to `docs/progress-archive/`.
- Git remains the truth for *code* changes; `PROGRESS.json` is the truth for *intent* (what's next, what's blocked, what was asked).

## Verify

1. Start a new session, run `/start-session` — the agent reports the current task, the last session's summary, and the health-check result without exploring the repo.
2. Interrupt a task, start another session — the new session resumes at the right step.
3. `/end-session` leaves `PROGRESS.json` updated and a commit whose message mentions the task id.

## Sources

- LIDR video B — "state" as the fourth harness area (prep table; persisted task artifact for resumption and hand-off) — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.9.
- Practitioner guide §6 — standardized startup routine, git log as the record, JSON over Markdown for progress — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.2.

## Change log
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).

- 2026-09-08 — created.
