---
description: Implement exactly one planned task with TDD and full verification. Usage: /develop-task T-003
---

Task: `$ARGUMENTS`. Read its entry in `PROGRESS.json` and the spec it links. Confirm you are in the task's worktree (`!git worktree list`). Work on this task only.

1. Restate the task in two sentences and list the files you will touch. If anything is unclear, ask and stop.
2. **Test first.** Write the test(s) named in the task. Run them: they must fail for the right reason. Show the failure.
3. **Implement** the minimum that makes them pass, following `docs/*-standards.md`. Nothing outside the task; note extras as new tasks instead.
4. **Verify**: `<<unit>>`, `<<integration if relevant>>`, `<<smoke e2e>>`, lint/format/type check. Paste a short summary of each result.
5. **Docs**: apply `docs/documentation-standards.md` §2; regenerate `docs/api-spec.yml` if routes changed.
6. Update `PROGRESS.json` (status `done` or `in_progress` with exact resume notes). Commit: `type(scope): summary ($ARGUMENTS)`.
7. Reply with the definition-of-done checklist from `docs/workflow.md` §2, each item marked with evidence. Stop.
