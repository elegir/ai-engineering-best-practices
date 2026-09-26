---
title: "Practices declare applicability with one plain-English line over a small vocabulary of observable facts; the agent infers the facts from the repo — no profile schema, no rule grammar, no rigor levels"
type: decision
status: accepted
date: 2026-09-26
tags: [decision, applicability, selector, project-profile, facts]
sources:
  - sources/2026-09-26-selector-debate.md
  - practices/facts.md
  - playbooks/which-practices-apply.md
supersedes: null
superseded-by: null
---

# 0003 — Applicability by facts

## Context

The KB must serve as a "guiding star": any repo consults it on day one and gets *only the practices that apply*. The first ten practices are working-style (they apply to any repo an agent works in); the fourteen practices coming from the AI-engineering course (RAG, vector stores, guardrails, multi-agent security, LLMOps…) are conditional on what the product does. On 2026-09-26 a research pass (AWS lenses, Google SRE, OWASP ASVS/SAMM, NIST profiles, Thoughtworks, Backstage/Cortex/OpsLevel scorecards, Azure workload guides, coding-agent rule mechanisms) produced a first design — a 12-dimension enum profile file per repo, a boolean rule grammar, a deterministic evaluator, per-topic rigor levels, a risk formula, fixture checks. An adversarial review (`sources/2026-09-26-selector-debate.md`) found it would fail on day one: nine of ten practices are honestly `always`; a solo owner answering twelve enum questions by voice would mis-profile every live product (the cold-email SaaS as `traffic: internal, data: none, autonomy: 1`); rigor defaulting to 1 would certify that security practices "do not apply" to the fintech and the multi-tenant SaaS; and a KB-defined file in every target repo contradicted decision 0001.

## Decision

1. Every practice declares `kind: working-style | capability` and `applies-when:` — **one plain-English line using only the vocabulary in `practices/facts.md`** (`always`, fact words, `and`/`or`/`not`). The same line appears as a column in `practices/README.md`, which is what an agent reads first. The prose "Applies when / Does not apply when" sections stay; they hold the technical reasons.
2. **Facts are observable, not self-reported.** Ten are inferred from the repo with evidence (an LLM SDK, a `tenant_id` column, a `send_email` client, a deploy config, tables with emails…); two workflow facts are asked. The agent shows "this is what I found" in one screen and Martin corrects it. There is no questionnaire.
3. **Safety attaches on facts, not on levels.** `acts_on_world`, `personal_data`, `regulated`, `multi_tenant` trigger the security/safety practices; nobody has to "raise a rigor level" for them to apply. The default is the safer one.
4. **No formula.** Ordering is a stated list (`practices/facts.md` §Ordering). No scores, no HIGH/MEDIUM/LOW.
5. **The KB writes nothing into target repos.** The facts and the resulting applies/skipped list are the *output* of `playbooks/which-practices-apply.md`, a markdown block Martin may keep in the repo's own docs. Decision 0001 stands unchanged.
6. **Every "skipped" carries a reason about this repo**, in the ASVS sense (a technical fact, not a preference or a lack of time).
7. **Golden-path bundles are deferred**: Martin's project shapes are recorded as worked examples in the decision guide; a shape becomes a copyable bundle only after it has been applied to two real repos.
8. **Maintenance is one file**: adding a fact word edits `practices/facts.md`; `playbooks/ingest-new-source.md` requires `kind` and `applies-when` for any new practice; `scripts/kb-check.sh` fails on missing fields, unknown words, or a practice missing from the README table.

## Consequences

- The conditional part of the KB stays honest and small; the working-style core is not artificially capped.
- The first real iteration — running `which-practices-apply.md` + `audit-repo-against-kb.md` on one of Martin's repos — is the next step, and its findings are what may justify more machinery later (bundles, inference scripts). Nothing is built ahead of that evidence.
- Rejected and recorded so they are not re-proposed without new evidence: profile schema file per repo, boolean grammar + evaluator script, rigor levels / `rigor-min`, risk formula, fixture-profile gates, core-size cap, re-trigger rule in target repos.
