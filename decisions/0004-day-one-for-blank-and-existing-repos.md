---
title: "0004 — Two entry doors, one router: a blank repo declares planned facts and is bootstrapped; an existing repo has its facts inferred and is audited; `applies.py` is the authority for selection and order; practices are promoted by adoption, principles by course confirmation; a new practice is routed only after the previous module's day-0 files passed Verify in a real repo"
type: decision
status: accepted
date: 2026-09-30
tags: [decision, day-one, bootstrap, planned-facts, bundles, promotion, router, acceptance-test, governance]
sources:
  - sources/2026-09-30-day-one-debate.md
  - decisions/0003-applicability-by-facts.md
  - decisions/0001-knowledge-base-structure.md
supersedes: null
superseded-by: null
---

# 0004 — Day one for blank *and* existing repos

## Context

The goal of this knowledge base, as Martin stated it on 2026-09-30, is that **any repository — a blank one on its first day or one that has run in production for a year — consults the KB, discovers by itself which practices apply to it, and starts from a complete, well-routed system of best practices**, with the KB improved continuously from the market and every source registered so nothing is paid for twice.

Decision 0003 (2026-09-26) built the selection mechanism for that goal: practices declare `applies-when` over a small vocabulary of *observable* facts, an agent infers the facts from the repo with evidence, and Martin confirms them in one screen. It explicitly rejected profile files, evaluator scripts as authority, bundles before two real instances, and any re-trigger mechanism in target repos. It was right about the existing-repo door: the first real run (AI SDR, 2026-09-28) found a product that *exposes* tools rather than calling them, a dormant Slack bot and two stale copies of the guide, and each finding improved the KB.

A clean-context devil's advocate attacked the goal on 2026-09-30 (`sources/2026-09-30-day-one-debate.md`, twenty attacks, two rounds). The attacks that survived rebuttal show that 0003 serves only one of the two doors:

- **A blank repo has nothing to observe.** Every inferred fact is "no", so the router returns the ten working-style practices and nothing else; the capability practices (LLM calls, gateway, context management, agent patterns) arrive only *after* code has been written without them — exactly the moment the KB was supposed to prevent.
- **The safety facts route to nothing.** `acts_on_world`, `personal_data`, `regulated`, `multi_tenant` and `brownfield` appear in no `applies-when` line, so a payments product and a marketing site receive identical lists, while the playbook claims that compliance "attaches on `regulated`".
- **No scaffold exists for a blank repo.** The audit inventories absences; the docs skeleton has twenty-four placeholders that presuppose decisions a day-one repo has not made.
- **Nothing is ever promoted.** Every capability practice is `draft` until a lecture date; the KB has zero field evidence that any copyable file works anywhere; "only trust `current`" makes the most valuable material officially untrustworthy.
- **The routing layer is prose evaluated by judgment** (`facts.md` says so) while a script parses it; the script's order differs from the playbook's; `security-baseline` is missing from the ordering lists.

## Decision

The KB has **two entry doors and one router**. Both doors produce the same artefact — a confirmed facts list — and the same router (`scripts/applies.py` over the `applies-when` lines) turns it into the practice list. What differs is where the facts come from and what happens next.

### 1. Facts carry a `source`: `inferred`, `planned` or `asked`

Every fact in a repo's facts list records how it was established. **Inferred** facts come from evidence in the code, as 0003 defined them. **Asked** facts are the workflow questions (`parallel_sessions`, `long_tasks`) plus, on a blank repo only, three intent questions a repo cannot show: *will it charge money or handle payments? will it serve several companies whose data must not mix? will it send, publish or pay without a human clicking each time?* **Planned** facts are what Martin states the product *will* do on a blank repo, captured from one paragraph of intent.

**Persistence rule.** A planned fact stays in force until **the code contradicts it or Martin drops it**. Inference can *upgrade* a planned fact to inferred (the vector store appears → `retrieval` becomes `inferred`); inference never deletes a planned fact just because the evidence is not there yet — that is the whole point of planning. A planned fact attaches only the **day-0** subset of a practice's files (see §3); the rest attaches when the fact is inferred.

### 2. The existing-repo door: infer, confirm, audit — unchanged from 0003

An existing repo (`brownfield`: real commits older than a few weeks, a schema with migrations, a deploy that runs) goes through `playbooks/which-practices-apply.md` as today: infer facts with evidence, confirm in one screen, list applies/skipped with reasons about *this* repo, then `playbooks/audit-repo-against-kb.md` on the practices that apply. `brownfield` is a **routing fact**: it selects the door, not a practice. Dormant-code rule, "never ask what the repo shows", and skip reasons about this repo all stand.

### 3. The blank-repo door: intent, planned facts, bundle, scaffold

A repo with no code goes through playbooks/bootstrap-new-repo.md (to be created): one paragraph of intent in Martin's words → planned facts (with the three intent questions above) → the router's list → the **bundle** for the resulting shape → the day-0 files copied and adapted (entry file, hooks, smoke test, facts block) → first commit. The bootstrap ships only files that have passed Verify somewhere (§6), which is why hooks are rewritten in Python to refuse running with an unreplaced placeholder, and why a TypeScript port of the day-0 LLM client exists before any bundle promises a TypeScript stack.

**Bundles** are the four shapes already used as worked examples (A multi-tenant agent SaaS that acts on the world; B scheduled LLM publishing pipeline; C site with no LLM at runtime; D payments/fintech). Each bundle has two parts: a **generated** practice list (from `applies.py`, so it cannot drift) and a **hand-written stack-defaults section** naming the variant folders to copy, which `kb-check.sh` validates against the folders that exist. This overturns 0003 §7 ("a shape becomes a bundle only after two real instances"): for a solo founder who starts a new shape rarely, the second instance never comes, and a generated list costs nothing to keep honest.

**Stack defaults** are recorded in a separate decision (proposed: Python/FastAPI for backends and pipelines, PHP/WordPress for sites, TypeScript for front-ends and Node services; pending Martin's confirmation).

### 4. The repo owns its facts file, via `agent-entry-file`

The confirmed facts list — with sources and evidence — lives in the target repo as a block that the `agent-entry-file` practice (`always`) carries, so it is present in every repo and re-read at every session start. The entry file's routine includes a **re-infer check**: at session start the agent compares the inferred facts to the code and reports a changed fact (a new `tenant_id` column, a new email client) instead of silently working from stale facts. This is the "re-trigger" 0003 §Consequences rejected; it is accepted now because the AI SDR run showed facts change (a bot switched off, an MCP server added) and nothing noticed.

Decision 0001 is **confirmed unchanged**: the KB writes nothing into target repos. The bootstrap and the audit *propose*; the repo copies, adapts and owns its files, including the facts block.

### 5. `applies.py` is the authority for selection and order

The `applies-when` lines are evaluated **mechanically** by `scripts/applies.py`, not "by the agent's judgment" as `practices/facts.md` said; the agent's judgment goes into establishing the facts and writing the skip reasons. The script also produces the **order** (working-style first in the README order, then capability practices by triggering fact, `security-baseline` included) and an `--explain` mode naming which fact fired each practice. Every practice gains `when: day-0 | first-user | at-scale`, so that a seven-file gateway practice does not land beside "can the agent run a test" on a repo that has no users. A **`ROUTER.md`** of at most 2 KB is generated from the practice frontmatter by `scripts/make-router.py`; `kb-check.sh` fails if it is stale; the skill points at it, so that routing costs an agent two kilobytes instead of fourteen thousand tokens of prose.

### 6. Promotion: practices by adoption, principles by course confirmation

A **practice** moves from `draft` to `current` only when a real repo has copied its files and its **Verify** section passed there, recorded in a field report (templates/field-report.md, to be created) and a row in practices/adoptions.md (to be created). A **principle** moves to `current` either the same way or when the course session on its topic confirms its content. Flow: field report → ingest (impact table) → adoptions row → status change.

**Routing gate.** From this decision on, a new practice enters `practices/README.md`'s table and the router **only after the previous module's day-0 files have passed Verify in one real repo**. Until then it exists as `draft`, unrouted (visible in its folder and in `INDEX.md`, absent from the router). Scans and digests continue at the course's pace; routing does not outrun evidence.

### 7. Safety facts select practices

Every fact word in `practices/facts.md` must select at least one practice or be declared a routing fact; `kb-check.sh` fails otherwise. Concretely: `security-baseline` is `always` for its core (secret scan, protected `.env`, dependency policy, dangerous-command guard) and escalates to its full part — threat model, injection fixture, MCP trust register, per-tenant keys and spend caps, trace redaction — when `acts_on_world or personal_data or regulated or multi_tenant`; `verification` gains a dry-run/approval section that applies when `acts_on_world`, because a product that moves money or sends email needs a sandbox mode as part of its sensor whether or not an LLM is involved.

### 8. Acceptance test for day one

Before module 4 is routed, two empty repos (shapes A and B) are bootstrapped through §3, timed, with token cost recorded and the transcript kept as a field report. This is the "fixture" 0003 rejected, justified now because the KB has had three modules and zero evidence that a copyable file works.

## Consequences

- Both doors benefit: a blank repo gets capability practices on day zero through planned facts and a bundle; an existing repo keeps evidence-based inference, gains safety routing it did not have, a facts block that stays in sync, and practices that are `current` because someone used them.
- `practices/facts.md`, `practices/README.md`, `playbooks/which-practices-apply.md` and `scripts/applies.py` change in the same series of publishes as this decision, in the order listed in `sources/2026-09-30-day-one-debate.md` §4; each publish is checked by `kb-check.sh`.
- More machinery than 0003 wanted: a frontmatter field or two, a router generator, a bootstrap playbook, a field-report template. Each exists because a specific attack showed the prose-only version failing, and each is kept honest by `kb-check.sh` rather than by memory.
- Overturned from 0003 and recorded here so they are not re-litigated without new evidence: §7 bundles-after-two-instances (→ generated bundles now); the rejection of a re-trigger in target repos (→ re-infer at session start, inside the repo's own entry file); "evaluated by judgment, not by a parser" (→ `applies.py` is the authority); `draft`-until-lecture (→ promotion by adoption). Still rejected: a profile schema per repo, rigor levels, a risk formula, a core-size cap.
- Deferred, recorded in the debate's "can wait" list: per-file `when:`; full TypeScript/PHP ports; an `owns:` line per practice; principle renumbering by topic; path resolution for cloud sessions; scan prioritisation by adoption; registry as JSONL; bilingual questions.
