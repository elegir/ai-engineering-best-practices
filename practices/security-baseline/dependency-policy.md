# Dependency policy (paste into docs/backend-standards.md §8 or docs/constitution.md)

1. An agent may **propose** a new dependency; only a human **approves** it. The proposal states: package name (exact), registry URL, version, weekly downloads / maintainers / last release date, why the standard library or an existing dependency is insufficient, license.
2. Verify the name resolves to the intended project (typosquats: `requests` vs `reqeusts`). Never install a package the agent "remembers" without checking the registry page.
3. Pin versions; lockfiles are protected files (agents cannot edit them directly — they run the package manager).
4. `<<npm audit / pip-audit / composer audit>>` runs on push; high/critical severity blocks.
5. Remove unused dependencies in the same PR that stops using them.
