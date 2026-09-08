# Startup routine (paste into AGENTS.md → "Start of every session")

1. Read `PROGRESS.json` (current task, notes, open questions) and `git log --oneline -15`.
2. Run the health check in `PROGRESS.json.meta.health_check`; if it fails, fix the environment first using `docs/development-guide.md`.
3. Confirm you are in the task's worktree; work on one task, one step at a time; update `PROGRESS.json` before stopping.
