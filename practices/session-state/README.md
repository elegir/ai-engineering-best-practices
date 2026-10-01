---
title: "Practice — session state (progress file + startup routine)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-30
tags: [state, progress, session, resumability]
kind: working-style
applies-when: "long_tasks or parallel_sessions"
reference-status: untested   # untested | field-tested | reference (decision 0005 §3)
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

## Reference implementation

`PROGRESS.json` + `startup-routine.md` + the two commands. The JSON shape is the reference, not a requirement: a repo that already tracks tasks (an issue tracker the agent can read) satisfies assertions 1–4 if the startup routine reads it.

## Stack-sensitive points

- Nothing in this practice depends on the product's stack; it depends on the **agent tool** (where commands live) and on the repo's health-check command, which comes from `../verification/`.
- Several worktrees (`../worktrees/`) need one progress file per task or a shared one with task scoping — decide once.

## Adapt

- Fill the `health_check` and test commands in `PROGRESS.json.meta`.
- If the repo uses an SDD tool (OpenSpec), tasks in `PROGRESS.json` reference the change/spec id rather than duplicating its task list.
- Decide who may edit `PROGRESS.json`: agents append to `sessions` and flip task `status`; humans edit `tasks`. Say so in `AGENTS.md`.
- Keep the file small: archive `sessions` older than 30 days to `docs/progress-archive/`.
- Git remains the truth for *code* changes; `PROGRESS.json` is the truth for *intent* (what's next, what's blocked, what was asked).

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

1. A new session, started with the startup routine, reports the current task, the last session's summary and the health-check result without exploring the repo — observer: agent — negative: the agent lists files or greps before reporting
2. A task interrupted mid-way and resumed in a new session continues at the recorded step, not from the beginning — observer: agent — negative: a redone step
3. Ending a session leaves the progress file updated and a commit whose message names the task id — observer: script — negative: a session that ends with the progress file unchanged
4. The progress file is valid JSON (or the repo's chosen format) and lists every task with an id, a status and a last-updated date — observer: script — negative: a task without a date, or invalid JSON

**Example commands (Claude Code):** `/start-session`; `/end-session`; `python3 -m json.tool PROGRESS.json`.

## Sources

- LIDR video B — "state" as the fourth harness area (prep table; persisted task artifact for resumption and hand-off) — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.9.
- Practitioner guide §6 — standardized startup routine, git log as the record, JSON over Markdown for progress — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.2.

## Change log

- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).

- 2026-09-08 — created.
