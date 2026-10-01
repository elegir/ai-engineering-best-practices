---
title: "Playbook — adopt a variant: turn a field report from a real repo into a field-tested variant of a practice, promote the reference, and record the adoption"
type: playbook
status: current
date: 2026-09-30
last-reviewed: 2026-09-30
tags: [variants, field-report, promotion, adoptions, stacks]
sources:
  - decisions/0005-contract-first-practices-and-stacks.md
  - sources/2026-09-30-stack-debate.md
supersedes: null
superseded-by: null
---

# Adopt a variant

**Who runs this.** An agent inside the knowledge base, when Martin brings a field report from a repo that implemented a practice (`practices/prompt-library/implement-practice.md` step 6). This is the only path by which code from a consumer enters the KB (decision 0005 §7): the consumer repo is the test bench; the KB is the author and owner of the variant.

**Output.** A source entry (the field report), a row in `practices/adoptions.md`, and — when the stack has no variant yet — `practices/<name>/variants/<stack>/` with frontmatter, plus status changes on the practice. All published through `playbooks/publish-change.md`.

## Step 0 — sync

`bash scripts/kb-sync.sh`; stop if not in sync.

## Step 1 — file the report as a source

Copy the report into `sources/YYYY-MM-DD-field-report-<repo>-<practice>.md` using `templates/field-report.md`. Check the mandatory numbers (§4): a report without tokens, minutes and errors-caught goes back to the repo's session with one question; do not fill them in by estimate.

## Step 2 — judge the contract, not the code

For each assertion in the report's §2: `pass` with evidence and the negative performed counts; `pass` without the negative is `unverified` and is said so; `n.a.` needs a technical reason about that repo. If any assertion turned out to be unjudgeable (the agent could not tell what "pass" meant), that is a defect in the practice's Verify — fix the assertion in the practice README with a change-log line, and bump `last-reviewed`.

## Step 3 — ingest the findings

Run §5 of the report through the impact table of `playbooks/ingest-new-source.md` step 2b. A missing stack-sensitive point becomes a bullet in the practice; a wrong placeholder is fixed; a package choice the agent had to make alone becomes a line in `stack-notes/<stack>.md` (create it if absent — fifteen lines, no code, no version pins).

## Step 4 — write the variant (new stack only)

If `practices/<name>/variants/<stack>/` does not exist and the report's §6 lists files: write the variant **in the KB** from those files — generalised (placeholders back in, repo names out), with a `README.md` whose frontmatter is:

```
---
title: "Variant — <practice> for <stack>"
status: field-tested        # field-tested | reference
verified-against: YYYY-MM-DD   # the practice's last-reviewed date at the time of the report
field-report: sources/YYYY-MM-DD-field-report-<repo>-<practice>.md
stack: <stack>
---
```

`scripts/kb-check.sh` [9/9] fails when `verified-against` is older than the practice's `last-reviewed`: a practice revised after the variant was tested needs the variant re-verified (a new report) or its status noted as stale in its README.

If the variant already exists: record the second adoption in `practices/adoptions.md`; update the variant only through a new field report.

## Step 5 — promote

- The **practice**'s `reference-status` moves `untested → field-tested` on the first report whose assertions all pass (or `n.a.` with reason) in the reference stack; the practice's `status` moves `draft → current` on the same event unless the README names another blocker.
- A **variant** moves `field-tested → reference` after a clean-context agent reviews it against the practice's negatives (every assertion's "negative" tried against the variant's files) within thirty days of the report; record the review as a source entry. There is no "second consumer" requirement.
- The router (`scripts/applies.py --explain`, `ROUTER.md`) shows the status of the reference and of each variant, so an adopting agent sees "field-tested" or "no reference yet" at adoption time.

## Step 6 — record and publish

Add a row to `practices/adoptions.md` (date, practice, repo, stack, outcome, report path, tokens). `INDEX.md` gets the source row. Publish: `bash scripts/kb-check.sh && bash scripts/kb-publish.sh adopt-<repo>-<practice> "<message>"`.

## Change log

- 2026-09-30 — created (decision 0005 §7; rebuttal to attack 10 in `sources/2026-09-30-stack-debate.md`: "through ingest" needed a named procedure).
