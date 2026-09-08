# Definition of done (paste into docs/workflow.md §2 and adapt the commands)

The agent verifies every item before saying "done". Items marked ⚙ are also enforced by hooks/CI.

- [ ] The task maps to a story/spec item (`<<specs/…>>`), and the change stays inside it.
- [ ] Tests were written **before** implementation and failed first (TDD).
- [ ] ⚙ Unit suite green: `<<npm test>>`; new/changed code coverage ≥ <<90>>%: `<<coverage cmd>>`.
- [ ] ⚙ Integration suite green: `<<cmd>>`.
- [ ] ⚙ Smoke e2e green: `<<npx playwright test e2e/smoke>>` / `<<hurl --test tests/api/smoke.hurl>>` / `<<pytest -q tests/test_smoke.py>>` / `<<npx bats test/cli.bats>>`.
- [ ] ⚙ Lint, format, type check clean; no rule disabled inline; no config changed.
- [ ] Security: dependency/secret scan run (`<<snyk test / npm audit / pip-audit>>`); no secrets in the diff.
- [ ] Docs updated per `docs/documentation-standards.md` §2; `docs/api-spec.yml` regenerated if routes changed.
- [ ] `PROGRESS.json` updated (status, notes on where things stand, open questions).
- [ ] ⚙ Commit follows Conventional Commits and references the task id; no `--no-verify`.
- [ ] PR description: what changed, why, how it was verified (paste the smoke command output summary), link to spec.
- [ ] Worktree noted for removal after merge.
