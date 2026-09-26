---
title: "Playbook — which practices apply to this repo: infer the facts with evidence, confirm in one screen, list applies / skipped with reasons, then audit"
type: playbook
status: current
date: 2026-09-26
last-reviewed: 2026-09-26
tags: [applicability, selector, day-one, facts, audit]
sources:
  - decisions/0003-applicability-by-facts.md
  - practices/facts.md
  - sources/2026-09-26-selector-debate.md
supersedes: null
superseded-by: null
---

# Which practices apply to this repo?

**Who runs this.** An agent inside the target repository, on Martin's request — on day one of a new repo or before the first audit of an existing one. It is the entry point; `audit-repo-against-kb.md` runs after it and only inspects the practices this playbook marked as applying.

**Output.** A short markdown block in chat (Martin may paste it into the repo's own `docs/`; this playbook writes nothing): the facts found with their evidence, the confirmed facts, and the practice list in two groups — *applies* (in order) and *skipped* (each with a reason about this repo). **No files are changed.**

**Rules.** Facts are inferred from the repo, never guessed from the project's name or Martin's description; each fact is shown with the evidence that supports it. Only two facts are asked (`parallel_sessions`, `long_tasks`), one question each. Everything else is one screen for Martin to correct. Never ask a question whose answer is visible in the repo.

## Step 1 — Infer the facts (read only)

For each **inferred** fact in `practices/facts.md`, look for the evidence listed there and record one of:

- `yes — <evidence: file or command output, one line>`
- `no — <what you looked for and did not find>`
- `unclear — <what you found and why it does not settle it>`

Typical commands: dependency manifests (`package.json`, `requirements*.txt`, `pyproject.toml`, `composer.json`), `.env.example`, `grep -ril "tenant_id\|org_id\|workspace_id" --include=*.sql --include=*.py --include=*.ts`, `grep -ril "smtp\|sendgrid\|resend\|mailgun\|wp-json\|stripe\|paypal"`, migrations/schema files for `email|phone|name|address` columns, deploy/infra files (`.do/app.yaml`, `Dockerfile`, `*.service`, cron, CI deploy jobs), `git log --oneline | wc -l` and the date of the first commit.

Then ask the two questions, one at a time, in plain words: "¿Corrés más de una sesión de Claude a la vez en este repo?" and "¿Las tareas acá suelen llevar más de una sentada?"

## Step 2 — Confirm in one screen

Show a table: fact · answer · evidence. Ask Martin to correct anything wrong. Pay attention to the three facts a solo owner most often under-reports, and state them explicitly with their evidence:

- `production` is **yes** for any system that already emails, publishes, charges or syncs on a schedule, even with no human users in a UI.
- `personal_data` is **yes** for contact lists, lead lists, message bodies — "business contacts" are people.
- `acts_on_world` is **yes** if the system sends, publishes or pays without a human clicking each time; that is the safety trigger, whatever the LLM does.

Stop until Martin confirms.

## Step 3 — Evaluate every practice

Read the `applies-when` column of `practices/README.md` (do not open every README yet). For each practice write one of:

- **applies** — the line holds for the confirmed facts.
- **skipped — reason** — the line does not hold; the reason must be a fact about *this* repo ("no retrieval: no vector store, no embeddings call, no corpus"), never a preference or a lack of time. Copy the practice's prose "Does not apply when" only if it literally describes this repo.
- **already present** — the repo has it (say where); the audit will judge the quality.

Order the *applies* list with the rule in `practices/facts.md` §Ordering. Do not add a score.

## Step 4 — Hand over

Print the block:

```
## KB applicability — <repo> — <date>
Facts: llm_calls=yes (…), retrieval=no (…), tools=yes (…), multi_agent=no, acts_on_world=yes (…), multi_tenant=yes (…), production=yes (…), personal_data=yes (…), regulated=yes (CAN-SPAM/TCPA: …), brownfield=yes, parallel_sessions=yes, long_tasks=yes
Applies (in order): verification, context-docs-skeleton, agent-entry-file, hooks-and-guards, session-state, prompt-library, spec-driven, worktrees, token-savings, agent-patterns, <capability practices…>
Skipped: rag-pipeline — no retrieval (no vector store, no embeddings, no corpus) · …
Already present: hooks-and-guards (.claude/settings.json, 4 hooks) · …
```

Then run `playbooks/audit-repo-against-kb.md` on the *applies* + *already present* lists only. Re-run this playbook when a fact changes (a `tenant_id` migration lands, a vector store is added, the first customer goes live).

## Worked examples — Martin's project shapes (facts → list)

These are the shapes his repos actually have (2026-09). They are examples for the agent, not templates to copy; a shape becomes a copyable bundle only after it has been applied to two real repos (decision 0003 §7).

**A. Multi-tenant agent SaaS that acts on the world** (cold-email system for law firms). Facts: `llm_calls`, `tools`, `acts_on_world` (sends email on a schedule), `multi_tenant` (customer workspaces), `production`, `personal_data` (lawyer contact lists, reply text), `regulated` (CAN-SPAM/TCPA consent), `brownfield`, `parallel_sessions`, `long_tasks`; `retrieval` = no unless a vector store exists; `multi_agent` = usually no. → All nine working-style practices; `agent-patterns/`; then, as they land: guardrails/structured outputs, agent security & permissions, tenant isolation, evals, LLMOps. Skipped: RAG/vector-store practices (no retrieval).

**B. Scheduled LLM publishing pipeline** (RSS → rewrite → WordPress). Facts: `llm_calls`, `acts_on_world` (publishes to public sites), `production`, `brownfield`; `tools` = no (one call with a fixed prompt), `retrieval` = no, `multi_tenant` = **no** (many sites, one owner), `personal_data` = usually no. → Working-style practices; then structured outputs/guardrails (output validation before publishing), prompt caching/cost, evals of output quality, LLMOps (cost per run). Skipped: `agent-patterns/` (no model-driven control flow — say so), RAG practices, tenant isolation.

**C. Content or marketing site with no LLM at runtime**. Facts: `production`, `brownfield` (or not); everything LLM-related = no. → Working-style practices only (the coding agent still needs verification, context docs, an entry file, hooks). Skipped: every capability practice, each with "no `llm_calls`: no model SDK, no API key, no prompts".

**D. Payments / fintech**. Facts: `regulated` (PCI/KYC), `personal_data`, `production`, `multi_tenant` if several merchants; LLM facts as found. → Working-style; the security-by-design and compliance practices attach on `regulated` regardless of whether an LLM is present.
