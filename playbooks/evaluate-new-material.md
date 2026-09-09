---
title: "Playbook — evaluate new material before it changes anything (the improvement gate)"
type: playbook
status: current
date: 2026-09-09
last-reviewed: 2026-09-09
tags: [gate, evaluation, quality, ingest]
sources:
  - principles/09-knowledge-base-design.md
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Evaluate new material — the improvement gate

Every piece of new material (a workshop, an article, a tool, a tip, a lesson from a failure) goes through this gate **before** any principle or practice is touched. The goal is that the knowledge base only gets better: nothing enters that is not better than what is there, that adds nothing, or that is worse than known alternatives. Rejections are recorded too, so the same idea is not re-evaluated next month.

## Step 0 — Always capture the raw material

Regardless of the verdict, save the raw material under `sources/raw/YYYY-MM-DD-slug/` and write the source entry (`templates/source-entry.md`). A rejected idea still gets a dated source entry — with `verdict: rejected` and the reason — because the *reasoning* is knowledge. The gate decides what happens to `principles/` and `practices/`, never whether the source is kept.

## Step 1 — Triage: what kind of thing is this?

| Kind | Examples | Goes to |
|---|---|---|
| **Concept / framing** | "harness = model + everything else", the context→harness→loop pyramid | `principles/` |
| **Applicable mechanism** | a hook, a config, a script, a doc skeleton, a prompt, a checklist | `practices/` (+ a `skills/` entry if it is a procedure an agent runs) |
| **Tool** | rtk, OpenSpec, Playwright MCP | `practices/` as a variant or option — never as *the* answer |
| **Number / benchmark / claim** | "Faros: incidents per PR +243%" | cited inside a source; enters a principle only as attributed evidence |
| **Decision for Martin's repos** | "all repos use worktrees per ticket" | `decisions/` |
| **Stack- or domain-specific mechanism** | a WordPress-only hook, a payments-only audit step | `practices/<name>/variants/` — the KB stays agnostic; specifics live as variants of an agnostic practice, never as a separate vertical |
| **Vendor pitch / marketing** | "use our framework" | source entry only, with the bias noted |

## Step 2 — Compare against what exists

Find the principle and the practice the material touches (`INDEX.md` topic map). Then answer, in writing, in the source entry's "Gate" section:

1. **What exactly would change?** Quote the current sentence/file and the proposed replacement or addition. If you cannot name the concrete change, the material adds nothing → `rejected: no delta`.
2. **Is it better than what is there?** Better means at least one of: stronger evidence, fewer tokens/less effort for the same result, more general (works in more stacks), safer, simpler to verify, or it fixes a known failure recorded in a harness changelog or a lesson. "Newer" and "popular" are not "better".
3. **Is it worse than a known alternative?** Check the alternatives already listed in the practice (e.g. OpenSpec vs Spec-Kit vs Superpowers). If the material is a weaker version of something already documented, record it as `rejected: dominated by <X>` with the comparison.
4. **Does it contradict a principle?** If yes, this is a *supersession* candidate, not an addition: it needs stronger evidence than the current text has, and it goes through `CONVENTIONS.md` §6 (mark superseded, never silently overwrite).

## Step 3 — Score (0–3 each; write the numbers in the source entry)

| Criterion | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **Evidence** | opinion / vendor claim | practitioner experience, one team | multiple independent teams or a primary write-up with numbers | controlled study or reproducible measurement |
| **Applicability** | one tool, one stack, one project | one stack family | most stacks with a variant | fully agnostic |
| **Delta vs current** | none | cosmetic | materially better on one criterion | better on several criteria or fixes a recorded failure |
| **Maturity / stability** | changes monthly, pre-1.0, "expect breaking changes" | young but stable API | established | boring and durable |
| **Cost to adopt** | days, infra, new dependencies | hours | minutes | copy a file |
| **Reversibility** | hard to undo | undoable with effort | easy to undo | trivially removable |

Verdict rules of thumb:

- **Adopt** (becomes/changes a principle and a practice): Delta ≥ 2 **and** Evidence ≥ 2 **and** not dominated by an existing alternative.
- **Refine** (small edit, new variant, extra example, added source citation): Delta = 1–2, any evidence, no contradiction.
- **Park** (source entry with `verdict: parked`, revisit date set): promising but Evidence ≤ 1 or Maturity = 0 — e.g. a tool that is three weeks old. Add a line to `INDEX.md` "Open actions" with the revisit date.
- **Reject** (source entry with `verdict: rejected` + reason): Delta = 0, or dominated, or evidence is only a vendor claim for a vendor's own product, or it weakens verification/safety to gain speed.

Anything that **removes a sensor** (tests, hooks, review) to gain tokens or speed is rejected by default, whatever the score.

## Step 4 — Write the verdict into the source entry

Add a `## Gate` section with: kind (Step 1), the concrete delta (Step 2), the six scores, the verdict, and — for adopt/refine — the exact files to change. Set the frontmatter `verdict:` to `adopted | refined | parked | rejected`.

## Step 5 — Only then, ingest

Continue with `playbooks/ingest-new-source.md` for adopt/refine. For parked and rejected: source entry + `INDEX.md` line, nothing else changes, publish.

## Step 6 — Periodic review (quarterly)

Run the gardening pass from `principles/09-knowledge-base-design.md`: principles with `last-reviewed` older than 90 days get re-checked against their sources; parked items past their revisit date get re-scored; practices whose tools moved (version bumps, renamed CLIs) get their variants refreshed. Each outcome is one publish.

## Examples of verdicts (so the standard is concrete)

- *"Use Opus for everything" (Boris Cherny) vs "Opus plans, Sonnet executes" (LIDR)*: both kept, recorded as a **contested** point in `principles/08-model-selection.md`, because evidence is practitioner-level on both sides and the reconciliation ("depends on how strong your context is") is itself useful. Verdict: refined.
- *A new token-compression tool with only its own README numbers*: **parked**, revisit in 60 days, or adopt only after a one-week measurement logged in `practices/token-savings/measurement-log.md` (that measurement then becomes a source with Evidence = 3).
- *"Skip e2e tests on small changes to save tokens"*: **rejected** — removes a sensor.
- *A second spec framework with the same delta-spec idea as OpenSpec but fewer integrations*: **rejected: dominated by OpenSpec**, noted as an alternative in the practice's README.
