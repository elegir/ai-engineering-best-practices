# Testing standards

<!-- Agents read this instead of inferring from existing tests. Be exact: commands, locations, thresholds, and what runs when. -->

## 1. Layers and what each proves
| Layer | Proves | Tool | Location | Runs |
|---|---|---|---|---|
| Unit | one function/module in isolation | `<<jest / pytest / phpunit>>` | `<<beside the code>>` | on every file edit (hook) and pre-commit |
| Integration | modules together against a real DB/queue in a container | same + `<<testcontainers / compose>>` | `<<tests/integration>>` | pre-commit (fast subset) and CI |
| End-to-end | the feature through the real interface | `<<Playwright / Hurl / bats>>` | `<<e2e/>>` | Stop hook (smoke) and CI (full) |
| Contract | API matches `api-spec.yml` | `<<schemathesis / dredd>>` | | CI |

## 2. Rules
- **TDD**: write the test, run it, see it fail, then implement. Do not write implementation first.
- Coverage on new/changed code ≥ **<<90>>%**; overall never decreases.
- Tests are independent, deterministic, and fast (unit < <<100 ms>> each). No sleeps; no real network.
- Test data: factories/fixtures in `<<location>>`; use the seed accounts listed in `development-guide.md` §4 for e2e.
- Structure: Arrange–Act–Assert; one behavior per test; name states the behavior (`returns 404 when user does not exist`).
- Mocks only at boundaries (network, time, randomness). Never mock the thing under test.
- An agent may **not** edit an existing assertion to make a test pass without a comment explaining the changed requirement and a link to the spec.

## 3. Anti-patterns (rejected in review)
- Tests that assert implementation details (call counts on internals).
- Snapshot tests of large structures with no review.
- Skipped/`only` tests committed.
- Flaky tests kept "for now".

## 4. Commands
```bash
<<unit>>           # e.g. npm test
<<integration>>    # e.g. npm run test:integration
<<e2e>>            # e.g. npx playwright test
<<coverage>>       # e.g. npm run test -- --coverage
```

## 5. When tests run automatically
- PostToolUse hook: formatter + linter (not tests).
- Pre-commit: unit + type check.
- Stop hook: e2e smoke.
- CI: everything; required to merge.

## 6. Writing e2e tests
- Prefer accessibility-tree selectors (`getByRole`, `getByLabel`) over CSS/XPath.
- One file per user flow; seed state via API or fixtures, not via clicking through.
- Generate candidate tests with the agent; keep them deterministic; run them without the agent in CI.

## 7. Examples
<<One GOOD unit test, one GOOD integration test, one GOOD e2e test from this repo, and one BAD example of each with the reason.>>
