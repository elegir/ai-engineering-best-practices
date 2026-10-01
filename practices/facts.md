---
title: "Facts — the controlled vocabulary that decides which practices apply to a repo"
type: template
status: current
date: 2026-09-26
last-reviewed: 2026-09-30
tags: [applicability, facts, selector]
sources:
  - decisions/0003-applicability-by-facts.md
  - decisions/0004-day-one-for-blank-and-existing-repos.md
supersedes: null
superseded-by: null
---

# Facts — the applicability vocabulary

Every practice declares `applies-when` in its frontmatter and in the table of `practices/README.md` as **one line that uses only the words below** (plus `always`, `and`, `or`, `not`, parentheses). A practice may add a second line, `full-when`, for a part of it that attaches on more facts than its core (today only `security-baseline`). **The lines are evaluated mechanically by `scripts/applies.py`** (decision 0004 §5); the agent's judgment goes into establishing the facts with evidence and into writing the reason for every skipped practice, never into reading the line differently. The vocabulary exists so that twenty-five practices written over a year by different agents call the same thing by the same name. Adding a word: add a row here, a change-log line below, and use it in at least one practice (or declare it a routing fact, below). `scripts/kb-check.sh` fails on an `applies-when`/`full-when` that uses a word not listed here, **and on a word listed here that no practice uses**.

Most facts are **inferred from the repo with evidence** by `playbooks/which-practices-apply.md`; the agent shows what it found and Martin corrects it in one screen. Two are **asked**, because they are about how Martin works, not about the code. On a blank repo, where there is nothing to infer, facts are **planned** from one paragraph of intent plus three intent questions (playbooks/bootstrap-new-repo.md, to be created); a planned fact stays until the code contradicts it or Martin drops it. Every fact a repo records carries its source: `inferred`, `planned` or `asked`.

| Fact | Means | Evidence the agent looks for (inferred) or the question (asked) |
|---|---|---|
| `llm_calls` | The product itself calls a language model at runtime (not just the coding agent working on the repo) | An LLM SDK in the lockfile/requirements (`anthropic`, `openai`, `google-genai`, `litellm`, `langchain`, `@ai-sdk/*`), API keys for a model vendor in `.env.example`, prompt files/templates |
| `retrieval` | The product answers or acts using documents/data fetched at query time by similarity or search | A vector store or `pgvector`, an embeddings call, chunking code, a document corpus folder, a search index (BM25, Elastic, Typesense) |
| `tools` | The model can decide to call functions/tools (function calling, MCP client, agent loop) | Tool/function schemas passed to the model, a `tool_use`/`function_call` loop, an MCP client config used at runtime, an agent framework (LangGraph, ADK, Agents SDK, Pydantic AI, Claude Agent SDK) |
| `multi_turn` | The product passes history back into the model — a conversation, a session with memory, or an agent loop — so the context grows across calls | A messages/threads/sessions table or store, a conversation id passed to the model call, history appended to the request, an agent loop (`tool_use` → result → call again) |
| `exposes_tools` | The product *serves* tools to an external agent (it is an MCP server, a function-calling API or a plugin) — the model that decides which tool to call lives outside the product, but the tool names, descriptions, schemas and error messages are the product's | An MCP server implementation (`FastMCP`, `@mcp.tool`, an `mcp_*_router`), a tools manifest, OpenAPI operations described for LLM consumption, a plugin manifest. (Found in the first real test: AI SDR exposes 100+ MCP tools to Claude Desktop and has no agent loop of its own.) |
| `multi_agent` | More than one model-driven agent runs in the same feature (orchestrator/subagents, handoffs) | Subagent spawning, orchestrator/worker roles, A2A, handoff definitions |
| `acts_on_world` | The product takes actions with effects outside the repo that are hard to undo: sends email/messages, publishes content, moves money, changes third-party records | SMTP/email API clients, social/CMS publish calls (WordPress REST, Slack post), payment SDKs, write calls to CRMs/ticketing; scheduled jobs that trigger them |
| `multi_tenant` | One deployment serves several *customers/organisations* whose data must not mix | A `tenant_id`/`org_id`/`workspace_id` column or foreign key across tables, per-tenant config, RLS policies, tenant-scoped API keys. (Many sites owned by one person is **not** multi-tenant; several paying customers is.) |
| `production` | Real users or real third parties depend on it now — including systems with no human UI that email, publish or charge on a schedule | A deploy config (App Platform spec, Dockerfile + host, systemd units, cron), a live domain in docs, a customer/tenant table with rows, monitoring/alerts |
| `personal_data` | It stores or processes data about identifiable people who are not the owner (names + emails, phone numbers, conversation text, addresses) | Tables/models with `email`, `phone`, `name`, `address`, message bodies; contact lists; CRM sync; consent/unsubscribe logic |
| `regulated` | The data or the activity falls under a specific regime: payments/PCI, health, finance/KYC, EU residents/GDPR, telecom consent (TCPA), cold-email law (CAN-SPAM) | Payment SDKs, KYC/AML libraries, health record fields, EU customers named in docs, consent/DNC tables, legal notices in the codebase |
| `brownfield` | **Routing fact.** There is existing code and existing users/data to protect (as opposed to a repo started this week). It selects the *door*, not a practice: `yes` → infer facts and audit (`playbooks/which-practices-apply.md` then `audit-repo-against-kb.md`); `no` → plan facts and bootstrap (playbooks/bootstrap-new-repo.md, to be created) | `git log` older than a few weeks with real commits; a schema with migrations; a deploy that already runs |
| `parallel_sessions` | **Asked.** Martin runs, or wants to run, more than one agent session on this repo at the same time (or a session while he edits) | Question: "Do you run more than one Claude session on this repo at once?" |
| `long_tasks` | **Asked.** Work on this repo regularly spans more than one session (features that take days) | Question: "Do tasks here usually take more than one sitting?" |

## Dormant code

A fact is inferred from what *runs*, not from what exists. Code that is switched off, feature-flagged off, or documented as retired (a bot "apagado desde 07-14") makes the fact `no — dormant since <date>: <evidence>`, so that a future reader sees why, and it is re-checked if the feature comes back. Added 2026-09-28 after the AI SDR test (`multi_turn` inferred from a dormant Slack bot).

## Ordering rule (implemented by `scripts/applies.py`, used by `which-practices-apply.md`)

1. Working-style practices first: `verification` → `context-docs-skeleton` → `agent-entry-file` → `hooks-and-guards` → `security-baseline` (core; its full part is listed again under step 2 when its `full-when` holds) → `session-state` → `prompt-library` → `spec-driven` → `worktrees` → `token-savings`.
2. Then capability practices and the full part of `security-baseline`, ordered by the fact that triggered them: `acts_on_world` → `personal_data` / `regulated` → `multi_tenant` → `production` → everything else.

There is no score. The list is the plan, and each skipped practice carries a reason *about this repo*.

## Change log
- 2026-09-30 — decision 0004: the lines are evaluated by `scripts/applies.py`, not by judgment; `full-when` added for a practice with an `always` core and a conditional full part; `brownfield` declared a routing fact (door selection); planned facts and the `inferred | planned | asked` source introduced; `security-baseline` added to the ordering rule; kb-check now also fails on a listed word no practice uses (debate attack 2, `sources/2026-09-30-day-one-debate.md`).
- 2026-09-26 — created with 12 facts (10 inferred, 2 asked) from the selector debate (`decisions/0003-applicability-by-facts.md`).
- 2026-09-27 — added `multi_turn` (inferred) for `practices/context-management/`; source `sources/2026-09-27-s02-context-caching-digest.md` row 36.
- 2026-09-28 — added `exposes_tools` (inferred) and the dormant-code rule; both from the first real run of `which-practices-apply.md` on AI SDR, which found a product that is a tool *provider* (MCP server with 100+ tools) rather than a tool *caller*, and a `multi_turn` signal that came only from a bot switched off in July.
