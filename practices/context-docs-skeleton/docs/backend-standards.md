# Backend standards

<!-- This is the long document (expect ~1,000 lines when complete). Every section must contain: the rule, WHY, a GOOD example, a BAD example. Agents copy examples; make them real code from this repo. Generate the first draft with prompts/generate-docs.md §3, then review. -->

## 1. Technical overview
Stack summary (link `stack.md`), runtime, framework, ORM, testing framework, dev tools (Postman/Hurl collection location).

## 2. Architecture principles applied
<<DDD? Hexagonal? Which principles concretely — e.g. "services never know about HTTP", "repositories return domain objects, not ORM rows".>> Link `architecture.md`. SOLID with examples from this codebase.

## 3. Project structure
Folder tree with one line per folder. Where new code goes for each kind of change.

## 4. API standards
- URL and resource naming; versioning; pagination; filtering.
- Request validation: <<library>>; validate at the edge, never trust input.
- Response envelope: <<shape>>; error format: <<shape with code, message, details>>.
- Status codes table.
- Authentication and authorization: where checks happen.
- OpenAPI: `docs/api-spec.yml` is regenerated from <<annotations/route definitions>> — never hand-edited.
- GOOD / BAD examples for one endpoint.

## 5. Database patterns
- Access only through repositories.
- Transactions: when and how.
- Migrations: tool, naming, reversibility, review rules.
- N+1 avoidance; indexes; query logging in dev.
- GOOD / BAD examples.

## 6. Error handling
- Error class hierarchy; what is thrown where; what is caught where (one place at the edge).
- Never swallow errors; never log-and-rethrow twice.
- User-facing vs internal messages.
- GOOD / BAD examples.

## 7. Logging and observability
- Structured logs (JSON), required fields (request id, user id where allowed), levels.
- What must never be logged (secrets, PII, tokens).
- Metrics/tracing if any.

## 8. Security
- Secrets only via environment; `.env` never committed; agents may not edit `.env`.
- Input validation, output encoding; SQL injection (parameterized only), XSS, CORS policy, CSRF, rate limiting.
- Dependency scanning: <<tool>>; how often.
- Auth token handling; password hashing; session policy.

## 9. Performance
- Budgets (p95 latency, memory) if defined; caching rules; background jobs vs request path.

## 10. Testing (summary — full rules in `testing-standards.md`)
- Unit tests beside code; integration tests against a real DB in a container; coverage ≥ <<90>>% on new code; tests run before every commit.

## 11. Git workflow
- Branch naming `<<type/ticket-short-desc>>`; branches start from `<<main>>`; rebase vs merge policy; commit message format (`<<conventional commits>>`); PR required for `<<main>>`; who reviews; squash or not; what must be green before merge.
- One worktree per ticket (see `development-guide.md` §5).

## 12. Code style
- Formatter and linter are the law; no inline disables without a comment referencing an ADR.
- Naming conventions; file size limits; comment policy (why, not what).
- Prohibited patterns (with the reason): <<`any` in TS; bare `except:` in Python; direct SQL in controllers…>>

## 13. Definition of done for backend changes
Code follows this document · tests per `testing-standards.md` · docs updated per `documentation-standards.md` · lint/type/security clean · migration reviewed · PR description links the spec.
