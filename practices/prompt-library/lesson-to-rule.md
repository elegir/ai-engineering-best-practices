---
description: Turn a mistake into an enforced rule (the ratchet). Usage: /lesson <what went wrong>
---

A mistake happened: $ARGUMENTS

Do not just apologize or add a sentence. Propose the **strongest feasible enforcement**, in this order of preference, and explain which you chose and why the stronger ones do not apply:

1. **Test** — a unit/integration/e2e test that would have failed. Write it.
2. **Linter/structural rule** — a rule (Biome/ESLint/Ruff/phpcs/ast-grep/import-linter) with an error message in the form `WHY: … FIX: … EXAMPLE: bad → good`.
3. **Hook** — a PreToolUse/PostToolUse/Stop or Lefthook check.
4. **Path-scoped rule** — `.claude/rules/<topic>.md` with `paths:` if it only matters in one area.
5. **Instruction line** — one line in `AGENTS.md` (only if 1–4 are impossible), phrased as a verifiable instruction, with a pointer to what enforces it.

Also: add a line to `docs/harness-changelog.md` (`YYYY-MM-DD — <mistake> → <mechanism added>`), and if the lesson is general (not repo-specific), say so — it may belong in the knowledge base (`../ai-engineering-best-practices/`) as a source entry.
