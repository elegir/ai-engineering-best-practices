---
description: Standard session end — verify, record progress, commit
---

Close the session cleanly:

1. Run the unit tests (`PROGRESS.json.meta.unit_tests`). If red, do not proceed; fix or record the failure in the task `notes` as "RED: <reason>".
2. Update `PROGRESS.json`: the current task's `status` and `notes` (exactly where to resume, in one or two sentences), append a `sessions` entry with date, task, summary, and the commit hashes you will create. Add any open question to `questions_for_martin`.
3. Check `docs/documentation-standards.md` §2: did this change require a doc update? If yes and it is not done, do it now.
4. Commit with a Conventional Commits message that includes the task id, e.g. `feat(auth): callback route for SSO sign-up (T-003)`. Never use `--no-verify`.
5. Reply with: task id, what was done, what is next, open questions, and the commit hash.
