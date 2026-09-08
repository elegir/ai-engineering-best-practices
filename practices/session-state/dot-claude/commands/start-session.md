---
description: Standard session start — load state, check health, pick the task
---

Run the startup routine and report back in under 15 lines. Do not start implementing.

1. Read `PROGRESS.json`. State: current task id and title, its `notes` (where we left off), any `questions_for_martin` without an answer.
2. Run `!git log --oneline -15` and `!git status --short`. Note uncommitted changes and whether they match the current task.
3. Run the health check from `PROGRESS.json.meta.health_check`. If it fails, diagnose using `docs/development-guide.md` and fix the environment before anything else; report what was wrong.
4. If the current task has a `worktree`, confirm we are in it (`!git worktree list`); if not, say so and stop.
5. Propose the next concrete step for the current task (one step, ≤ 1 hour). Wait for confirmation.
