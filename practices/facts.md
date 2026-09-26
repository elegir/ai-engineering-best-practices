---
title: "Facts — the controlled vocabulary that decides which practices apply to a repo"
type: template
status: current
date: 2026-09-26
last-reviewed: 2026-09-26
tags: [applicability, facts, selector]
sources:
  - decisions/0003-applicability-by-facts.md
supersedes: null
superseded-by: null
---

# Facts — the applicability vocabulary

Every practice declares `applies-when` in its frontmatter and in the table of `practices/README.md` as **one plain-English line that uses only the words below** (plus `always`, `and`, `or`, `not`). The line is evaluated by the agent's judgment, not by a parser; the vocabulary exists so that twenty-five practices written over a year by different agents call the same thing by the same name. Adding a word: add a row here, a change-log line below, and use it in at least one practice. `scripts/kb-check.sh` fails on an `applies-when` that uses a word not listed here.

Most facts are **inferred from the repo with evidence** by `playbooks/which-practices-apply.md`; the agent shows what it found and Martin corrects it in one screen. Two are **asked**, because they are about how Martin works, not about the code.

| Fact | Means | Evidence the agent looks for (inferred) or the question (asked) |
|---|---|---|
| `llm_calls` | The product itself calls a language model at runtime (not just the coding agent working on the repo) | An LLM SDK in the lockfile/requirements (`anthropic`, `openai`, `google-genai`, `litellm`, `langchain`, `@ai-sdk/*`), API keys for a model vendor in `.env.example`, prompt files/templates |
| `retrieval` | The product answers or acts using documents/data fetched at query time by similarity or search | A vector store or `pgvector`, an embeddings call, chunking code, a document corpus folder, a search index (BM25, Elastic, Typesense) |
| `tools` | The model can decide to call functions/tools (function calling, MCP client, agent loop) | Tool/function schemas passed to the model, a `tool_use`/`function_call` loop, an MCP client config used at runtime, an agent framework (LangGraph, ADK, Agents SDK, Pydantic AI, Claude Agent SDK) |
| `multi_agent` | More than one model-driven agent runs in the same feature (orchestrator/subagents, handoffs) | Subagent spawning, orchestrator/worker roles, A2A, handoff definitions |
| `acts_on_world` | The product takes actions with effects outside the repo that are hard to undo: sends email/messages, publishes content, moves money, changes third-party records | SMTP/email API clients, social/CMS publish calls (WordPress REST, Slack post), payment SDKs, write calls to CRMs/ticketing; scheduled jobs that trigger them |
| `multi_tenant` | One deployment serves several *customers/organisations* whose data must not mix | A `tenant_id`/`org_id`/`workspace_id` column or foreign key across tables, per-tenant config, RLS policies, tenant-scoped API keys. (Many sites owned by one person is **not** multi-tenant; several paying customers is.) |
| `production` | Real users or real third parties depend on it now — including systems with no human UI that email, publish or charge on a schedule | A deploy config (App Platform spec, Dockerfile + host, systemd units, cron), a live domain in docs, a customer/tenant table with rows, monitoring/alerts |
| `personal_data` | It stores or processes data about identifiable people who are not the owner (names + emails, phone numbers, conversation text, addresses) | Tables/models with `email`, `phone`, `name`, `address`, message bodies; contact lists; CRM sync; consent/unsubscribe logic |
| `regulated` | The data or the activity falls under a specific regime: payments/PCI, health, finance/KYC, EU residents/GDPR, telecom consent (TCPA), cold-email law (CAN-SPAM) | Payment SDKs, KYC/AML libraries, health record fields, EU customers named in docs, consent/DNC tables, legal notices in the codebase |
| `brownfield` | There is existing code and existing users/data to protect (as opposed to a repo started this week) | `git log` older than a few weeks with real commits; a schema with migrations; a deploy that already runs |
| `parallel_sessions` | **Asked.** Martin runs, or wants to run, more than one agent session on this repo at the same time (or a session while he edits) | Question: "Do you run more than one Claude session on this repo at once?" |
| `long_tasks` | **Asked.** Work on this repo regularly spans more than one session (features that take days) | Question: "Do tasks here usually take more than one sitting?" |

## Ordering rule (used by `which-practices-apply.md`)

1. Working-style practices first, in the order `practices/README.md` already gives (`verification` → `context-docs-skeleton` → `agent-entry-file` → `hooks-and-guards` → `session-state` → `prompt-library` → `spec-driven` → `worktrees` → `token-savings`).
2. Then capability practices, ordered by the fact that triggered them: `acts_on_world` → `personal_data` / `regulated` → `multi_tenant` → `production` → everything else.

There is no score. The list is the plan, and each skipped practice carries a reason *about this repo*.

## Change log
- 2026-09-26 — created with 12 facts (10 inferred, 2 asked) from the selector debate (`decisions/0003-applicability-by-facts.md`).
