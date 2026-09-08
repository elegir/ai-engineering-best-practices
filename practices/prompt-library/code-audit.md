---
description: Self-review the current diff against standards and spec before committing. Usage: /audit
---

Audit the uncommitted changes (`!git diff` and `!git diff --cached`) before any commit. Do not change code during the audit; produce findings.

Check, section by section, and report `file:line` for every finding or "none found":

1. **Spec**: every change maps to the current task in `PROGRESS.json`; nothing outside scope.
2. **Standards**: violations of `docs/backend-standards.md` / `docs/frontend-standards.md` (layering, error handling, logging, naming, prohibited patterns).
3. **Tests**: new behavior has tests written first; no weakened assertions; no skipped tests; coverage command result: `!<<coverage cmd>>`.
4. **Security**: secrets, unvalidated input, raw SQL, PII in logs, new dependencies without justification.
5. **Docs**: `docs/documentation-standards.md` §2 — which docs must change; are they changed?
6. **Simplification**: dead code, duplication, over-engineering (YAGNI); propose the smallest cleanups.
7. **Verification evidence**: results of `!<<unit>>`, `!<<lint>>`, `!<<smoke e2e>>`.

End with a verdict: READY TO COMMIT / FIX FIRST (list), and the proposed Conventional Commits message.
