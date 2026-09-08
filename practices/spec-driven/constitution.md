# Constitution — non-negotiable rules for <<PROJECT>>

<!-- One page max. Every plan and every task must respect these; a spec that conflicts is wrong, not the constitution. Cite the standards doc or ADR behind each rule. -->

1. **Architecture.** Layers and import direction per `docs/architecture.md` §2. No business logic in routes/controllers; no DB access outside repositories.
2. **Data.** Every schema change is a reversible migration; no destructive migration without a data-migration plan and backup step. `docs/data-model.md` updated in the same change.
3. **Security.** Secrets only via environment; input validated at the edge; parameterized queries only; auth through the shared middleware; dependency scan clean before merge.
4. **Testing.** TDD; new-code coverage ≥ <<90>>%; smoke e2e green before "done"; no skipped tests committed; assertions are never weakened to pass.
5. **Docs.** `docs/*` updated per `documentation-standards.md` §2; API spec regenerated, never hand-edited.
6. **Process.** Spec → plan → approval → one task at a time → verify. One ticket = one worktree = one branch. PR required for `<<main>>`. No `--no-verify`.
7. **Scope.** YAGNI: build only what the current story needs. Extras become new tasks.
8. **Tooling.** Formatter/linter configs and hooks are changed only by Martin. Prohibited libraries: see `docs/stack.md` "Do not use".
9. **Observability.** Structured logs with request id; never log secrets or PII.
10. **Ask, don't guess.** Ambiguity → question in `PROGRESS.json` → stop.
