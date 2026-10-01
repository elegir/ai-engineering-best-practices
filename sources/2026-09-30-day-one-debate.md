---
title: "Debate — does the KB meet the day-one goal? A clean-context devil's advocate attacks how the KB routes practices to repos today; two rounds; agreed changes before module 4"
type: source
status: current
date: 2026-09-30
tags: [debate, devil-advocate, applicability, day-one, bootstrap, bundles, planned-facts, promotion, router, governance]
sources:
  - decisions/0003-applicability-by-facts.md
  - playbooks/which-practices-apply.md
  - practices/facts.md
  - scripts/applies.py
supersedes: null
superseded-by: null
---

# Debate — the day-one goal, attacked

## 1. Context

**Goal under test (Martin, 2026-09-30).** Any repo of any project — including a blank repo on day one — consults this KB, discovers by itself which practices apply given the project's own characteristics, and starts from zero with a complete, well-routed system of best practices; the KB is improved continuously from the market and every source is registered so nothing is paid for twice.

**Method.** A devil's-advocate agent with clean context (no access to this session's reasoning) was given the goal and the repo at commit `1907218` (after modules 1, 2, 3 and 12 and the first real selection run on AI SDR, 2026-09-28), told to attack *how* the goal is pursued today, and to propose the strongest alternative per attack. Round 1: 20 attacks. Round 2: the author's concede / partly / defend per attack, and the advocate's rebuttal with a must-change-before-module-4 list. Both rounds are summarised below; the full exchange is in this session's transcript.

## 2. Round 1 — the attacks (condensed)

| # | Attack | Evidence |
|---|---|---|
| 1 | On a blank repo every inferred fact is "no", so the router returns the generic working-style list; capability practices arrive only after code was written without them | `which-practices-apply.md` "never guessed from the project's name or Martin's description"; `applies.py` with no facts |
| 2 | The safety facts (`acts_on_world`, `multi_tenant`, `personal_data`, `regulated`, `brownfield`) appear in **no** `applies-when` line; shapes C and D get identical lists; the playbook's claim that compliance "attaches on `regulated`" is false today | `practices/README.md` table; `applies.py --shapes` |
| 3 | Deferring bundles "until a shape has two instances" is the wrong test for a solo founder who starts a new shape rarely | decision 0003 §7 |
| 4 | Nothing produces a *scaffold* for a blank repo; the audit inventories absences and the docs skeleton has 24 placeholders that presuppose decisions | `audit-repo-against-kb.md`, `context-docs-skeleton/` |
| 5 | No day-0 / first-user / at-scale dimension: `llm-gateway` (7 files) lands all at once beside "can the agent run a test" | `facts.md` ordering rule; audit "top 7" |
| 6 | "Only trust `current`" + every capability practice `draft` until a lecture date = the most valuable material is officially untrustworthy for months | AGENTS.md; principles 10, 11, 12, 21 |
| 7 | `facts.md` says lines are evaluated by judgment, `applies.py` parses them; the script's order ≠ the playbook's ordering rule; `security-baseline` missing from the ordering lists | `facts.md` §Ordering, `applies.py` |
| 8 | Fact inference is fragile (`production` from a Dockerfile) and nothing detects a changed fact; a re-trigger was rejected by 0003 | `facts.md`, 0003 §5 |
| 9 | The two asked facts are workflow trivia; the intent questions (charge money? serve companies? act alone?) are the ones a repo cannot show; questions hardcoded in Spanish | `which-practices-apply.md` |
| 10 | Capability practices are mostly markdown policy; code is Python only; "TypeScript is a direct port" ships no port; no PHP anywhere | `llm-gateway/`, `llm-api-calls/` |
| 11 | Hook scripts are fragile (sed-parsed JSON, `<<…>>` placeholders parse as heredocs if left in, bash on a Windows machine) | `hooks-and-guards/` |
| 12 | Practice overlap (context budget in two folders; retry logic in two; tracing in two) with no conflict check | digests s2/s3 |
| 13 | One principle per course session will sprawl (21 numbered by session) | `scan-log.md` |
| 14 | Reading the routing layer costs ~14k tokens; the skill's topic map is stale and routes "apply" straight to the audit | AGENTS/INDEX/README/facts/playbooks sizes; `skills/…/SKILL.md` |
| 15 | Everything assumes a sibling folder and a local clone; cloud sessions break | `adopt-kb-in-a-repo.md` |
| 16 | The one consumer test (AI SDR) left no source entry | `sources/` |
| 17 | The KB never measures its own usefulness (adoptions) | `kb-check` tests structure only |
| 18 | Vendor talks are the input; Martin's own incidents are not | scan protocol |
| 19 | The registry (275 KB, 497 items after 4 modules) will become a merge bottleneck | `media-registry.json` |
| 20 | Everything waits on one person; 3 modules → 3 drafts, 0 promoted | — |

**What the advocate would not change:** facts as observable evidence with one confirmation screen; the working-style/capability split; skip reasons about *this* repo; `kb-sync.sh`; impact tables; never paying twice and reusing transcripts; the `verification` practice (the most copyable folder); `applies.py --shapes` in `kb-check`.

## 3. Round 2 — responses and rebuttals

| # | Author's response | Advocate's rebuttal (kept) |
|---|---|---|
| 1 | Concede: facts get a `source` (inferred / planned / asked); blank repo → one paragraph of intent → `planned` facts | A planned fact stays until **code contradicts it or Martin drops it**; inference can upgrade, never delete. Planned facts attach only the **day-0** subset |
| 2 | Concede: kb-check fails on unused fact words; `security-baseline` splits into an `always` core and a full part on the safety facts; dry-run/approval rule for `acts_on_world` | `brownfield` must select something or be dropped; the dry-run rule belongs in **`verification`** (conditional on `acts_on_world`), not in `llm-gateway` — the fintech moves money with no LLM |
| 3 | Partly: ship shapes A–D as **generated** draft bundles (cannot drift) | A generated list is not a bundle; pair it with a **hand-written stack-defaults section** that kb-check validates against existing variant folders |
| 4 | Concede: `bootstrap-new-repo.md` — intent → planned facts → bundle → stack defaults → entry file + hooks + smoke test → first commit | **Contradiction with 10 and 11**: the bootstrap would ship the fragile hooks and promise a TS stack with no TS client. Minimum before shipping: Python hooks that refuse to run with an unreplaced placeholder, and a TS port of the day-0 LLM client only. Stack defaults need a **decision record** |
| 5 | Concede: `when: day-0 / first-user / at-scale` per practice and per file in capability practices | Per-practice now; per-file can wait |
| 6 | Concede: `current` on adoption with Verify passed OR course confirmation | Split: a lecture can promote a **principle**; only adoption promotes a **practice** |
| 7 | Concede: `applies.py` is the authority for selection and order; `--explain` | — |
| 8 | Partly: the repo's own `docs/kb-facts.md` via `session-state`, re-inferred at session start; the KB still writes nothing | `session-state` is conditional; put the facts block in **`agent-entry-file`** (`always`), and the re-infer check in whichever routine is `always` |
| 9 | Partly: three intent questions on greenfield; keep the two workflow questions on brownfield; bilingual | — |
| 10 | Concede the gap, defer the ports to a consumer | See 4: the TS day-0 client cannot wait |
| 11 | Defer with a ticket | See 4: hooks must be fixed before any bootstrap ships them |
| 12 | Partly: `owns:` line per practice; re-home `context-budget.md` | Can wait |
| 13 | Concede: topics not sessions; soft cap ~15; stated in principle 09 | Can wait |
| 14 | Concede: generated `ROUTER.md` ≤ 2 KB; skill points at it | — |
| 15 | Concede: `$AIKB_PATH` → sibling → shallow clone | Can wait (sibling works today) |
| 16 | Concede: templates/field-report.md (to be created); AI SDR report when steps 4–5 arrive | "When they arrive" is not a date; the KB has **zero evidence any copyable file works anywhere** |
| 17 | Concede: practices/adoptions.md (to be created) | Name the flow: field report → ingest → adoptions row |
| 18 | Concede: lessons from own repos first in every module cycle | Cheap; do it |
| 19 | Defer JSONL until a merge conflict | — |
| 20 | Defend partly: cadence = one real application test every 3 modules | That test is **due now**. Compromise: scans and digests continue; a new practice is **not routed** (not in the README table / router) until the previous module's day-0 files passed Verify in one real repo |

**Not addressed by the author until the rebuttal:** no acceptance test for day one (bootstrap two empty repos, shapes A and B, timed, transcripts kept as field reports — the "fixture" 0003 rejected, now justified); no decision record for the overturns of 0003 §5, §7 and its rejected-options list; nobody measures what a bootstrap costs in tokens.

## 4. Agreed — what must change before module 4 (in order)

1. **Decision 0004** recording what this debate overturns in 0003 (planned facts; generated bundles with a validated stack section; the repo's own facts file via `agent-entry-file`; promotion by adoption for practices; `applies.py` as authority; the day-one acceptance test), and confirming 0001 unchanged (the KB writes nothing into target repos — the repo copies and owns its files).
2. **Safety routing**: kb-check fails on fact words no practice uses; `security-baseline` = `always` core + full part on `acts_on_world or personal_data or regulated or multi_tenant`; `verification` gains a dry-run/approval section conditional on `acts_on_world`; `brownfield` wired to the bootstrap-vs-audit fork or dropped.
3. **`applies.py` as the authority**: selection + ordering (security-baseline included), `when:` per practice (`day-0 | first-user | at-scale`), `--explain`; `facts.md` wording fixed; **`ROUTER.md`** generated from frontmatter (≤ 2 KB), kb-check fails if stale, skill points at it.
4. **Planned facts** with the persistence rule; **bundles** A–D (generated list + hand-written, validated stack defaults); **`bootstrap-new-repo.md`**; the facts block as part of `agent-entry-file`; a **stack-defaults decision** (Python/FastAPI, PHP/WordPress, TypeScript); **Python hooks** refusing unreplaced placeholders; a **TypeScript port of the day-0 LLM client** only.
5. **Acceptance test**: bootstrap two empty repos (shapes A and B), timed, token cost recorded, transcripts kept as field reports (templates/field-report.md (to be created)).
6. **Finish the AI SDR test**: apply at least one capability practice through Verify; field report; first row of practices/adoptions.md (to be created) (flow: field report → ingest → adoptions row).

**Routing gate (from 20):** from now on a new practice enters the README table and the router only after the previous module's day-0 files have passed Verify in one real repo; until then it exists as `draft`, unrouted.

**Can wait:** per-file `when:`; full TS/PHP ports (written when a consumer appears); `owns:` rule; principle renumbering (rule stated in 09 now); path resolution for cloud sessions; scan prioritisation by adoption; registry as JSONL; bilingual questions.

## 5. Opinions recorded as opinions

The advocate's view that a company-wide WIP limit should block new scans was not adopted; the routing gate is the compromise. The author's view that TS/PHP ports should wait for a consumer was adopted except for the day-0 client, because a bootstrap that promises a stack must ship that stack's first file. Both are judgment calls recorded here so a later reader knows they were considered.
