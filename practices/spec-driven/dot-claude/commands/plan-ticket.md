---
description: Plan a spec into atomized tasks — no code. Usage: /plan-ticket specs/<feature>.md
---

Use plan mode. Do not create or edit any file except the spec's "Clarifications" and "Task list" sections, and only after step 3.

1. **Read** `$ARGUMENTS`, `specs/constitution.md`, `docs/architecture.md`, `docs/testing-standards.md`, and `docs/workflow.md`. Read the code areas the spec touches.
2. **Ask the expert.** List every question you need answered before you could plan safely: ambiguous behavior, edge cases, data-model impacts, security, migration/rollback, non-functional needs, what is out of scope. Group by story. Stop and wait for answers. Do not assume.
3. **Spec review.** Rewrite unclear stories; ensure every acceptance criterion is testable and names its test file; flag anything that conflicts with the constitution. Record the answers under "Clarifications resolved" in the spec.
4. **Task list.** Produce tasks `T-NNN`, each: title, files to touch, test to write first, verification command, effort ≤ <<2 h>>, dependencies. Order so each task leaves the suite green. Add them to the spec's "Task list" and to `PROGRESS.json` as `todo`.
5. **Model note.** State which tier should execute each task (routine → mid tier; cross-module/refactor/security → top tier).
6. Present the plan and stop. Implementation happens only via `/develop-task` after approval.
