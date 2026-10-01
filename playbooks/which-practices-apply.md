---
title: "Playbook — which practices apply to this repo: infer the facts with evidence, confirm in one screen, list applies / skipped with reasons, then audit"
type: playbook
status: current
date: 2026-09-26
last-reviewed: 2026-09-30
tags: [applicability, selector, day-one, facts, audit]
sources:
  - decisions/0003-applicability-by-facts.md
  - decisions/0004-day-one-for-blank-and-existing-repos.md
  - practices/facts.md
  - sources/2026-09-26-selector-debate.md
supersedes: null
superseded-by: null
---

# Which practices apply to this repo?

**Who runs this.** An agent inside an **existing** target repository, on Martin's request, before its first audit. It is the entry point for the existing-repo door; `audit-repo-against-kb.md` runs after it and only inspects the practices this playbook marked as applying. A repository with **no code yet** takes the other door — `playbooks/bootstrap-new-repo.md` (decision `decisions/0004-day-one-for-blank-and-existing-repos.md` §3) — where facts are *planned* from intent instead of inferred. The routing fact `brownfield` decides: real commits older than a few weeks, a schema with migrations or a deploy that runs → this playbook; none of those → the bootstrap. Both doors end in the same router, `scripts/applies.py`.

**Output.** A short markdown block in chat (Martin may paste it into the repo's own `docs/`; this playbook writes nothing): the facts found with their evidence, the confirmed facts, and the practice list in two groups — *applies* (in order) and *skipped* (each with a reason about this repo). **No files are changed.**

**Rules.** Facts are inferred from the repo, never guessed from the project's name or Martin's description; each fact is shown with the evidence that supports it. Only two facts are asked (`parallel_sessions`, `long_tasks`), one question each. Everything else is one screen for Martin to correct. Never ask a question whose answer is visible in the repo.

## Step 0 — Is the guide current?

Run `bash <kb>/scripts/kb-sync.sh --pull`. It writes only inside the guide's `.git/` and fast-forwards the guide when it is merely behind — allowed even in a read-only session, because the guide is not the repo under review. Stop and tell Martin only if it reports `ahead` or uncommitted changes. Re-run it if the session lasts hours: the guide moves. (2026-09-28.)

## Step 1 — Infer the facts (read only)

For each **inferred** fact in `practices/facts.md`, look for the evidence listed there and record one of:

- `yes — <evidence: file or command output, one line>`
- `no — <what you looked for and did not find>`
- `unclear — <what you found and why it does not settle it>`

Typical commands: dependency manifests (`package.json`, `requirements*.txt`, `pyproject.toml`, `composer.json`), `.env.example`, `grep -ril "tenant_id\|org_id\|workspace_id" --include=*.sql --include=*.py --include=*.ts`, `grep -ril "smtp\|sendgrid\|resend\|mailgun\|wp-json\|stripe\|paypal"`, migrations/schema files for `email|phone|name|address` columns, deploy/infra files (`.do/app.yaml`, `Dockerfile`, `*.service`, cron, CI deploy jobs), `git log --oneline | wc -l` and the date of the first commit.

Then ask the two questions, one at a time, in plain words: "¿Corrés más de una sesión de Claude a la vez en este repo?" and "¿Las tareas acá suelen llevar más de una sentada?"

A fact inferred only from **dormant** code (a feature switched off or retired, per the repo's own docs) is `no — dormant since <date>`; see `practices/facts.md` §Dormant code. A product that *serves* tools to an external agent (MCP server, function-calling API) is `exposes_tools`, not `tools`.

## Step 2 — Confirm in one screen

Show a table: fact · answer · evidence. Ask Martin to correct anything wrong. Pay attention to the three facts a solo owner most often under-reports, and state them explicitly with their evidence:

- `production` is **yes** for any system that already emails, publishes, charges or syncs on a schedule, even with no human users in a UI.
- `personal_data` is **yes** for contact lists, lead lists, message bodies — "business contacts" are people.
- `acts_on_world` is **yes** if the system sends, publishes or pays without a human clicking each time; that is the safety trigger, whatever the LLM does.

Stop until Martin confirms.

## Step 3 — Evaluate every practice

Run `python3 <kb>/scripts/applies.py --explain <fact> <fact> …` with the confirmed facts: its output **is** the list and the order, each practice tagged with its `when` (day-0 | first-user | at-scale) and the status of its reference (`untested` until a field report exists — then implement from the contract with `practices/prompt-library/implement-practice.md`) (decision 0004 §5; the `applies-when` column of `practices/README.md` is what it evaluates, so you may read the column, but you do not re-interpret it). A practice with a `full-when` line is printed as `(core)` or `(full)` — today `security-baseline`: its full part (threat model, injection fixture, trust register) attaches on `acts_on_world or personal_data or regulated or multi_tenant`. A file inside an `always` practice may still be conditional, stated in that practice's README — today `verification/dry-run-and-approval.md`, only when `acts_on_world`. For each practice write one of:

- **applies** — the line holds for the confirmed facts.
- **skipped — reason** — the line does not hold; the reason must be a fact about *this* repo ("no retrieval: no vector store, no embeddings call, no corpus"), never a preference or a lack of time. Copy the practice's prose "Does not apply when" only if it literally describes this repo.
- **already present** — the repo has it (say where); the audit will judge the quality.

Keep the script's order (`practices/facts.md` §Ordering). Do not add a score.

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

**A. Multi-tenant agent SaaS that acts on the world** (cold-email system for law firms — confirmed on the real repo 2026-09-28). Facts: `llm_calls`, `exposes_tools` (an MCP server with 100+ tools; no agent loop of its own, so `tools` = no), `acts_on_world` (sends email and writes to the CRM on a schedule), `multi_tenant` (customer workspaces with RLS), `production`, `personal_data` (contact lists, reply text), `regulated` (CAN-SPAM, LFPDPPP), `brownfield`, `parallel_sessions`, `long_tasks`; `retrieval` = no (no vector store, embeddings or corpus); `multi_turn` = no — dormant since 2026-07 (Slack bot switched off); `multi_agent` = no. → Working-style: all ten (`context-docs-skeleton`, `agent-entry-file`, `hooks-and-guards`, `session-state`, `worktrees`, `verification`, `spec-driven`, `prompt-library`, `token-savings`, `security-baseline`). Capability, in the ordering rule: `llm-gateway/` (acts_on_world + production: fallback, keys per tenant, model registry), `agent-patterns/` (exposes_tools: the tool-design half), `llm-api-calls/`; then, as they land: structured outputs/guardrails (S4), tenant isolation, evals, LLMOps. Skipped: `context-management/` — no `multi_turn` (bot dormant) and no `retrieval`; RAG practices — no retrieval.

**B. Scheduled LLM publishing pipeline** (RSS → rewrite → WordPress). Facts: `llm_calls`, `acts_on_world` (publishes to public sites), `production`, `brownfield`; `tools` = no (one call with a fixed prompt), `exposes_tools` = no, `multi_turn` = no, `retrieval` = no, `multi_tenant` = **no** (many sites, one owner), `personal_data` = usually no, `parallel_sessions`/`long_tasks` as answered. → Working-style: eight (`session-state` and `worktrees` only if the two asked facts are yes). Capability: `llm-api-calls/` (one client module, versioned prompt, caching order), `llm-gateway/` (production: fallback and timeouts for a scheduled job that must not silently stall, model registry); then structured outputs/guardrails (output validation before publishing, S4), evals of output quality, LLMOps (cost per run). Skipped: `agent-patterns/` — no model-driven control flow and no tools exposed (say so); `context-management/` — single-shot calls, no history, no retrieval; RAG practices; tenant isolation.

**C. Content or marketing site with no LLM at runtime**. Facts: `production`, `brownfield` (or not); everything LLM-related = no. → Working-style practices only — the coding agent still needs verification, context docs, an entry file, hooks and the security baseline. Skipped: every capability practice, each with "no `llm_calls`: no model SDK, no API key, no prompts".

**D. Payments / fintech**. Facts: `regulated` (PCI/KYC), `personal_data`, `production`, `multi_tenant` if several merchants; LLM facts as found. → Working-style incl. `security-baseline/`; the security-by-design and compliance practices attach on `regulated` regardless of whether an LLM is present; capability practices only when the LLM facts are found.

These four lists are produced mechanically by `python3 scripts/applies.py --shapes` from the `applies-when` lines in `practices/README.md`; `scripts/kb-check.sh` runs it so the examples cannot drift from the practices (they did between 2026-09-26 and 2026-09-30). The script is a helper: the agent still writes the evidence and the repo-specific reasons.

## Change log

- 2026-09-30 (later) — `applies.py --explain` named as the output; `when` and reference status shown; `ROUTER.md` referenced.
- 2026-09-30 — decision 0004: this playbook is now the *existing-repo* door; blank repos go to `playbooks/bootstrap-new-repo.md`; `brownfield` is the routing fact; `scripts/applies.py` is the authority for the list and its order; `security-baseline` prints core/full; `verification/dry-run-and-approval.md` noted as conditional on `acts_on_world`.
