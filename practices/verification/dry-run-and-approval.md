# Dry run and approval — the sensor for products that act on the world

**Applies when `acts_on_world`** (the product sends email or messages, publishes content, moves money or changes third-party records without a human clicking each time). It does not matter whether an LLM is involved: a cron job that charges cards needs this exactly as much as an agent that drafts emails. Copy this file to `<repo>/docs/dry-run-and-approval.md` and treat its three rules as part of the definition of done.

## Why it is a verification concern

A smoke test proves the code path runs. For an irreversible action that is not enough: the test must prove the path runs **and stops before the effect** unless explicitly allowed. Without a dry-run mode the agent cannot verify a sender or a publisher at all — it either skips the test (no sensor) or sends for real (the incident). Source: `principles/05-verification-loops.md`; the "pipelines with side effects" line in `README.md` §Adapt of this practice; the "LLM opinion guarding an irreversible action" rule in `practices/llm-api-calls/failure-modes-and-mitigations.md`.

## Rule 1 — every side-effecting entry point has a dry-run mode

- One switch, named the same everywhere: an environment variable `<<DRY_RUN_VAR>>` (for example `PUBLISH_MODE=dry` — the same name the pytest fixture in `python-pytest/conftest.py` sets) **or** a CLI flag `--dry-run`. Not both, and never a per-module boolean someone forgets.
- In dry-run mode the code does everything up to the effect — renders the email, builds the payment request, prepares the CMS payload — and then **logs the payload and returns** a result object that says `dry_run=true`. The payload goes to the log or to an outbox table, where the test can read it.
- The default in every non-production environment is dry run. Real sending requires the switch to be set on purpose (`<<DRY_RUN_VAR>>=live`) **and** the environment to be production; the code refuses `live` outside production with a one-line error.
- If the code has no dry-run mode today, **adding it is the first task** of the audit, before any other practice touches the senders.

## Rule 2 — approval before the first live run of anything new

- A new template, a new recipient list, a new publishing target, a new price or a changed amount is first run in dry-run mode and the produced payload is shown to a human (Martin) in one screen: *what would be sent, to whom, how many*. Only after an explicit "go" does the switch move to live.
- Record the approval where the code can check it: a row in an approvals table, a dated line in `docs/harness-changelog.md`, or a tag — whatever the repo already has. The agent must not be able to flip `live` by itself: add the file that holds the switch's default to `protected_paths` in `.claude/hooks.json` (`practices/hooks-and-guards/`), so the edit is blocked before it happens.
- Volume guard: the first live run of a new thing is capped (`<<FIRST_RUN_CAP>>`, for example 10 recipients or 1 post) and the cap is lifted by a second approval, not by editing the number.

## Rule 2b — confidence-gated approval with a time-boxed window (added 2026-10-01)

- When the output that triggers the action carries a **confidence** — a probability from a classifier, a decision model or a log-probability read, never a number the generative model wrote (`../structured-outputs/decision-vs-generation.md`) — a **threshold in code** decides which actions wait for a human and which proceed: above `<<AUTO_THRESHOLD>>` (for example 0.90) the action runs under the dry-run and volume rules above; below it the payload goes to the approval queue.
- The queue has a **time-boxed window** (`<<APPROVAL_WINDOW>>`, for example 2 hours): an item approved inside the window is sent; an item that expires is **not** sent by default and is logged as expired — never "approved by silence" for anything irreversible. (Bhardwaj's shape at Developer Summit 2026-06 — "give them like one hour or two hours just to validate… if it is correct, agent will automatically send it out" — is recorded with the default inverted for safety: his version sends on expiry; this KB's does not, as an opinion for products that move money or email third parties.)
- The threshold and the window are **numbers in code with a test**, not prompt text; changing them is a reviewed commit, and the smoke test of rule 3 asserts that an item below the threshold lands in the queue and that an expired item did not send.
- Thresholds are per action class (a `<<send_email>>` may run at 0.85, a `<<charge>>` never auto-runs); the table of classes lives beside `<<DRY_RUN_VAR>>`'s default and is protected the same way. Source: `../../sources/2026-10-01-s04-structured-outputs-digest.md` row 22 (Bhardwaj; Boundary's thresholds-in-code).
- **The paused action is serialised run state** (added 2026-10-01, s5): what waits in the queue is the proposed tool call with its arguments, the calling identity, the window and the resumable state of the run, stored durably, so the approval survives a restart and the run resumes *from that state* on the decision — "that's still the same run" (OpenAI Agents SDK, read 2026-10-01). **Fail closed when review is unavailable**: a reviewer that cannot be reached, a queue that is down or a window that expires all mean *not sent* — the Agents SDK's "fail closed if review times out or becomes unavailable" agrees with this KB's inverted default. Source: `../../sources/2026-10-01-s05-context-memory-permissions-evals-digest.md` row 36; map in `../memory-and-permissions/permission-model.md` §4.

## Rule 3 — the smoke test runs the real path in dry-run mode

- `tests/` (or `e2e/`) contains at least one test per side-effecting entry point that runs it with the switch in dry-run mode, then asserts on the captured payload: recipient, subject, amount, target site — the three or four fields that, if wrong, hurt.
- The same test asserts that the effect **did not happen**: the mail client mock received no call, the outbox has `status=dry`, the payment SDK was not invoked. A dry-run mode that still sends is the worst outcome; test for it.
- This test is part of the smoke command that the Stop hook runs (`README.md` §Adapt). It must run in under a few seconds with no network.

## Adapt

- `<<DRY_RUN_VAR>>`: the repo's single switch. If there are several entry points (email, CRM write, publish), they all read the same switch.
- `<<FIRST_RUN_CAP>>`: the cap for a first live run; choose the number below which a mistake is embarrassing rather than expensive.
- `<<AUTO_THRESHOLD>>`, `<<APPROVAL_WINDOW>>` (rule 2b): only when the action is gated by a confidence; delete the rule otherwise.
- Where approvals are recorded: pick the place the repo already uses; do not add a table only for this.

## Verify

1. Run every side-effecting entry point with the switch unset in a non-production environment → nothing leaves; the log shows the payload with `dry_run=true`.
2. Set the switch to live outside production → the process refuses to start, with a one-line message naming the switch.
3. The smoke suite contains the dry-run tests from rule 3 and fails when a payload field is wrong or when the mock effect is called.
4. `docs/harness-changelog.md` (or the repo's equivalent) shows the approval line for the last new template/target/amount that went live.
5. (rule 2b, when a confidence gates the action) An item below `<<AUTO_THRESHOLD>>` lands in the approval queue and an item that passed `<<APPROVAL_WINDOW>>` unanswered did not send — both asserted by the smoke test.
