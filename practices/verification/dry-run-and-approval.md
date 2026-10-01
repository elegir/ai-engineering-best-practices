# Dry run and approval — the sensor for products that act on the world

**Applies when `acts_on_world`** (the product sends email or messages, publishes content, moves money or changes third-party records without a human clicking each time). It does not matter whether an LLM is involved: a cron job that charges cards needs this exactly as much as an agent that drafts emails. Copy this file to `<repo>/docs/dry-run-and-approval.md` and treat its three rules as part of the definition of done.

## Why it is a verification concern

A smoke test proves the code path runs. For an irreversible action that is not enough: the test must prove the path runs **and stops before the effect** unless explicitly allowed. Without a dry-run mode the agent cannot verify a sender or a publisher at all — it either skips the test (no sensor) or sends for real (the incident). Source: `principles/05-verification-loops.md`; the "pipelines with side effects" line in `README.md` §Adapt of this practice; the "LLM opinion guarding an irreversible action" rule in `practices/llm-api-calls/failure-modes-and-mitigations.md`.

## Rule 1 — every side-effecting entry point has a dry-run mode

- One switch, named the same everywhere: an environment variable `<<DRY_RUN_VAR>>` (for example `SEND_MODE=dry`) **or** a CLI flag `--dry-run`. Not both, and never a per-module boolean someone forgets.
- In dry-run mode the code does everything up to the effect — renders the email, builds the payment request, prepares the CMS payload — and then **logs the payload and returns** a result object that says `dry_run=true`. The payload goes to the log or to an outbox table, where the test can read it.
- The default in every non-production environment is dry run. Real sending requires the switch to be set on purpose (`SEND_MODE=live`) **and** the environment to be production; the code refuses `live` outside production with a one-line error.
- If the code has no dry-run mode today, **adding it is the first task** of the audit, before any other practice touches the senders.

## Rule 2 — approval before the first live run of anything new

- A new template, a new recipient list, a new publishing target, a new price or a changed amount is first run in dry-run mode and the produced payload is shown to a human (Martin) in one screen: *what would be sent, to whom, how many*. Only after an explicit "go" does the switch move to live.
- Record the approval where the code can check it: a row in an approvals table, a dated line in `docs/harness-changelog.md`, or a tag — whatever the repo already has. The agent must not be able to flip `live` by itself: add the file that holds the switch's default to `protected_paths` in `.claude/hooks.json` (`practices/hooks-and-guards/`), so the edit is blocked before it happens.
- Volume guard: the first live run of a new thing is capped (`<<FIRST_RUN_CAP>>`, for example 10 recipients or 1 post) and the cap is lifted by a second approval, not by editing the number.

## Rule 3 — the smoke test runs the real path in dry-run mode

- `tests/` (or `e2e/`) contains at least one test per side-effecting entry point that runs it with the switch in dry-run mode, then asserts on the captured payload: recipient, subject, amount, target site — the three or four fields that, if wrong, hurt.
- The same test asserts that the effect **did not happen**: the mail client mock received no call, the outbox has `status=dry`, the payment SDK was not invoked. A dry-run mode that still sends is the worst outcome; test for it.
- This test is part of the smoke command that the Stop hook runs (`README.md` §Adapt). It must run in under a few seconds with no network.

## Adapt

- `<<DRY_RUN_VAR>>`: the repo's single switch. If there are several entry points (email, CRM write, publish), they all read the same switch.
- `<<FIRST_RUN_CAP>>`: the cap for a first live run; choose the number below which a mistake is embarrassing rather than expensive.
- Where approvals are recorded: pick the place the repo already uses; do not add a table only for this.

## Verify

1. Run every side-effecting entry point with the switch unset in a non-production environment → nothing leaves; the log shows the payload with `dry_run=true`.
2. Set the switch to live outside production → the process refuses to start, with a one-line message naming the switch.
3. The smoke suite contains the dry-run tests from rule 3 and fails when a payload field is wrong or when the mock effect is called.
4. `docs/harness-changelog.md` (or the repo's equivalent) shows the approval line for the last new template/target/amount that went live.
