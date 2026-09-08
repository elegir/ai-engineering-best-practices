---
paths:
  - "<<src/routes/**/*.ts>>"
  - "<<src/api/**/*.py>>"
---

# API rules (loaded only when editing API files)

- Validate every request body and query with `<<zod / pydantic>>` schemas defined in `<<src/schemas>>`; never read raw input in handlers.
- Use the standard error envelope from `docs/backend-standards.md` §4; never `res.status(500).send(err.message)`.
- Every new route: update `docs/api-spec.yml` by running `<<regen command>>`, add an integration test in `<<tests/integration/api>>`, and an e2e or Hurl check if user-facing.
- Auth: handlers never check tokens themselves; use the `<<requireAuth>>` middleware.
