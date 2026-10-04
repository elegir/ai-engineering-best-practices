---
title: "Agent design and tools — an agent is a model calling well-designed tools in a loop; decide first whether you need one"
type: principle
status: draft              # draft until LIDR session 12 (2027-01-14) is ingested and compared
date: 2026-09-24
last-reviewed: 2026-10-04
tags: [agents, workflows, tool-design, function-calling, mcp, agentic-rag, react, s12]
sources:
  - sources/2026-09-24-s12-agents-digest.md
  - sources/2026-09-24-market-scan-s12-intro-to-agents.md
  - https://www.anthropic.com/engineering/building-effective-agents
  - https://www.anthropic.com/engineering/writing-tools-for-agents
  - https://modelcontextprotocol.io/specification/latest
supersedes: null
superseded-by: null
---

# Agent design and tools

## 1. The question this answers

When a feature needs a language model to *do* something rather than answer once, how do we decide between a fixed pipeline and an autonomous agent, what is the smallest correct shape of an agent, and how do we design the tools it uses so that it actually works?

## 2. Short answer

Distinguish two things. A **workflow** is code that calls the model a fixed number of times in a fixed order; an **agent** is a model given tools and an open-ended goal that decides for itself how many steps to take. Build a workflow whenever the decision tree can be drawn, latency matters, or the budget per task is cents. Build an agent only when the task is ambiguous, valuable, verifiable, and its errors are cheap to discover — and then keep it to the minimal shape: an environment, a set of tools, a system prompt, and the model called in a loop. Spend your iteration on those three components before adding orchestration. Most of the leverage is in **tool design**: tools should return what a person would see (not one call per API endpoint), be documented as carefully as the prompt, return errors as text the model can act on, and use formats the model already knows. Expose tools through a CLI when a coding agent has a terminal, through MCP when you need a narrow, tightly-permissioned agent, and through skills when the thing to share is a procedure. Read the raw context the model receives and ask the model to critique it; most "agent bugs" are missing context or a bad tool. And close the loop with a signal (tests, a checker, an eval), because an agent without feedback does not converge.

## 3. Long explanation

### 3.1 Workflow or agent? The checklist

The vocabulary comes from Anthropic's *Building Effective Agents* (2024-12) and its authors' talks (`sources/2026-09-24-s12-agents-digest.md` §3.1). A workflow chains narrow prompts (classify → draft → format) through code that knows exactly what happens next; an agent gets a goal, tools and permission to loop until it decides it is done. Neither is "better": the workflow trades flexibility for control, cost and latency; the agent trades those for the ability to handle situations you could not enumerate.

Barry Zhang's four questions decide it:

1. **Complexity.** Can you map the decision tree? Then build it explicitly and optimise each node; that is cheaper and gives you control. Agents earn their cost in ambiguous problem spaces.
2. **Value.** Exploration costs tokens. If the budget per task is ~10 cents you have ~30–50k tokens; a high-volume support flow should be a workflow that covers the common cases.
3. **Critical capabilities.** Before trusting an agent, prove the model can do the two or three things the trajectory depends on (for coding: write, debug, recover from its own errors). If it cannot, reduce scope and retry rather than adding scaffolding.
4. **Cost of error and of error discovery.** If errors are expensive *and* hard to notice, autonomy must be limited (read-only tools, approvals), which also limits how far the agent can scale.

Coding passes all four — ambiguous, valuable, models already good at it, verifiable by tests and CI — which is why coding agents were the first to work in production. By late 2025 Anthropic's own message shifted: for tasks where absolute quality matters, agent loops now outperform workflows because models respond to feedback; workflows remain right for low latency and single-shot answers. The practical reconciliation, and this KB's position: *the default moved toward loops for quality-critical work; the four questions still decide, and the answer is often a **workflow of agents** — a fixed pipeline whose every step is itself a small closed loop (write the SQL, run it, look, fix, then hand off) instead of a single shot that passes a broken result downstream.*

### 3.2 The minimal agent

Three components and a loop: the **environment** (the system the agent acts in), the **tools** (its interface to act and to get feedback), the **system prompt** (goal, constraints, ideal behaviour), and the model called repeatedly until it stops calling tools. Three very different production agents at Anthropic share almost the same code; the environment is given by the use case, so the only two design decisions are *which tools* and *which prompt*. Everything else — caching the trajectory, parallelising tool calls, showing progress to the user — is optimisation to do after the behaviour is right, because complexity added early kills iteration speed and makes observability harder. The academic version is the ReAct loop (observe → plan → act, names vary by paper); Google ADK's version distinguishes sequential, reactive and planning agents and lets you wrap an LLM agent in a loop agent with a checker and a retry cap. See `practices/agent-patterns/agent-loop-skeleton.py` for the loop in ~60 lines and `patterns-catalogue.md` for the composable patterns (prompt chaining, routing, parallelisation, orchestrator–workers, evaluator–optimiser; Ng's reflection / tool use / planning / multi-agent).

### 3.3 Think like your agent

Every serious practitioner in the scan repeats this. At each step the model knows only what is in its context window — 10–20k tokens of system prompt, tool schemas, tool results — and nothing else. Builders design from their own perspective, then are puzzled by the agent's choices. The fix is mechanical: dump exactly what the model receives and read it as if you knew nothing else (Zhang's team literally closed their eyes for a minute and then blinked at one screenshot to understand a computer-use agent); print every tool call's *parameters* — what the model chose to search for — and every *result*; then ask the model itself: "Is anything here ambiguous? Can you follow it? Does this tool need more or fewer parameters? Why did you decide this at step 7, and what would have helped?" A model reviewing its own trajectory is not a substitute for your understanding, but it closes the gap fast. Prompt: `practices/prompt-library/trajectory-review.md`.

A second habit from the vendor APIs (`sources/2026-09-27-s01-llm-setup-digest.md` §3.2): keep the model's *own reasoning* in the loop — pass reasoning items back on the next turn (OpenAI reports better tool use and lower latency; Anthropic's thinking blocks work the same way) — so that the model sees its plan and you can read it when a trajectory goes wrong.

### 3.4 Tool design

This is where most of the new knowledge in the scan lives, and where most agent failures live ("99 % of the time it's a bug in one of the tools" — Notion).

Two rules from the session-2 scan (`sources/2026-09-27-s02-context-caching-digest.md` §3.2–3.3) sit on top of everything below. **Return an identifier with, or instead of, the payload** (a path, URL, query or record id): a result that is addressable can later be dropped from the transcript and re-read on demand, which is what makes context compaction lossless. And **keep the tool set fixed within a session**: loading and unloading tool schemas per turn invalidates the provider's prompt cache and leaves the model remembering tools that no longer exist (Manus). Progressive disclosure of tools (below) is therefore done *between* sessions or through a search-tools tool whose own schema is stable — or, Manus's way, with a small fixed set of atomic functions ("try not to include more than 30") plus a sandboxed shell with `--help` and a code tool that reach everything else without changing the schema.

- **A tool is one-to-one with your UI, not your API.** If understanding a Slack thread takes three endpoints (conversation, user-id → name, channel-id → name), a model given three tools must make three calls and stitch the result; a person sees it rendered once. Design the tool to return what the person would see, with the surrounding context, in one call. The model is a *user*, not a program.
- **Document tools the way you would for a colleague.** Descriptions and parameter docs are part of the prompt and shape the rest of it. Parameters named `a` and `b` with no docstring fail for the model as they would for an engineer. Put domain hints in the description ("search for the runbook when the user mentions an incident").
- **Give the model formats it already knows.** Notion replaced a lossless custom XML of its block model with a lossy, simple markdown, and a bespoke JSON query language with SQLite — because models know markdown and SQL and had to be prompted into the internal formats. Expose no unnecessary internal complexity.
- **Return errors, do not raise them.** A raised exception ends the loop; a returned human-readable message lets the model read it and correct course. Bound every tool: request limits per run, maximum lines per read, paths confined to an allowed root.
- **Fewer, better tools; disclose progressively.** Vercel's 80 %-fewer-tools case (`02-harness-engineering.md`) is confirmed from every side: models cope with roughly 50–100 tool schemas, quality degrades before the context is full, and any engineer adding a niche tool can make the whole agent worse by over-triggering it. Bucket tools among subagents (~20 each), or add a *tool-search* tool / router that loads full schemas on demand. Avoid name collisions across servers.
- **Describe by goal, not by example.** Notion dropped few-shot examples entirely: modern models instruction-follow well, and goal-driven descriptions let each product team own its tool definition *and its evals* instead of five people guarding one prompt string. If you must tune a description, iterate it with a reasoning model against an eval set of (request → expected tool call) pairs rather than by hand.
- **Verify auth is not the weakest link.** An agent using its own credentials has no notion of the user; OAuth impersonation leaves long-lived tokens on disk; the mature pattern is token exchange (agent authenticated, acting on behalf of the user) with a vault issuing short-lived credentials — detail in the session-14 material. At minimum: know which rung of that ladder each tool is on.

A tool call is itself a structured output that deterministic code dispatches — "there's nothing special about tools, it's just JSON and code" (Horthy, 12-Factor factor 4); mark tools `strict` where the provider supports it, because constrained decoding removes hallucinated tool names and malformed arguments (Pokrass, 2024-09; Anthropic docs 2026-10-01); and the "description is prompt" rule extends to every output schema, with two official places for instructions — the system message says *when*, the field description says *how* — and a descriptive key name as a help (the key-name trick is swyx's habit, not officially endorsed by Pokrass; `principles/13-structured-outputs-and-guardrails.md` §3.1).

Template and checklist: `practices/agent-patterns/tool-definition-template.md`.

### 3.5 How to expose tools: CLI, MCP, skill, RAG, memory

MCP standardises three primitives, each with a different controller: **tools** (the model decides when to call), **resources** (the application decides what to attach; can be dynamic and subscribable), **prompts** (the user invokes them, like slash commands); plus *sampling* (a server asks the client for a completion while the client keeps control of model, cost and privacy) and *composability* (a server can itself be a client, so agents chain). Roadmap items from the March 2025 launch talk — remote servers with OAuth, the registry, `.well-known` discovery, tool annotations such as read-vs-write, namespacing — are in the 2026-07-28 specification; go to the spec, not the talk, for what exists.

The 2026 debate is not whether MCP works but when to use it. Notion's Simon Last, after five harness rebuilds: **CLIs** are better for coding agents — they run in the terminal (pagination, cursors), give progressive disclosure for free (`--help`), and are *bootstrapped*: the agent can debug and fix its own tool in the same environment, whereas a broken MCP transport leaves the agent with nothing. **MCP** is better for a narrow, lightweight agent without a compute runtime and when a tight permission model matters ("all you can do is call the tools"; a CLI raises real questions about token exfiltration). It is also wasteful to pay a model to renegotiate a deterministic integration on every call. Claude's own guidance agrees operationally: MCP tool definitions sit in context even unused, so disable what you do not use, prefer a CLI (`gh`, `aws`, `wp-cli`) where one exists, and package CLI usage as a **skill** so the instructions load only when relevant. IBM's rule of thumb completes the picture: knowledge someone *wrote down* → RAG; knowledge the agent *learned from experience* → memory; a repeatable *procedure* with judgment about when to escalate → skill; reaching *out into the world* → MCP. Decision table: `practices/agent-patterns/tool-transport-decision-table.md`.

The permission model for the MCP branch is Block's (Angie Jones, 2026-01, a regulated company rolling out an MCP client to ~12,000 employees): an **allow-list of servers admitted by security review** ("if it's not on that allow list… the agent will say nope, can't install it"), **destructive-tool annotations with a mandatory approval** (non-destructive tools run freely; a destructive one must "ask my permission first"), and **OAuth through the company identity provider** instead of API keys and scopes; her Council of Mind demo is MCP *sampling* in use (a server borrowing the user's model for nine persona calls). Her cross-system examples (an incident that pages a human while an agent opens a PR; an agent in Slack implementing the chosen fix) are all narrow, hosted and permissioned — consistent with Notion's split. Detail: `15-memory-external-context-and-permissions.md` §3.4–3.5; `practices/memory-and-permissions/permission-model.md`.

Whatever you choose, keep one internal abstraction (`tool`, `agent`, `completion`, `integration`) so that MCP is one integration type among others and the framework can be replaced; every team that has shipped at scale has rebuilt theirs several times.

### 3.6 Agentic RAG

Classic semantic RAG (embed → retrieve → one LLM call) is not dead: it wins on latency and cost. Agentic RAG wins on quality because the loop can self-correct when the first search misses. The minimal, framework-free version is three tools over a folder of markdown — `list_files`, `grep` (ripgrep), `read_file` with a line cap — and a structured output with citations (file, quote, line). These are exactly the primitives coding agents use over a codebase; the same loop works over a Postgres table of documents. The framework version (LangGraph) adds a *grade documents* step and a *rewrite query* branch — confirmed by Lance Martin's CRAG, Self-RAG and adaptive-RAG flows (grade the documents → rewrite the query or fall back to web search → grade the answer for hallucination → grade it against the question; 2024-04, `yt-sVcwVQRHIc8-…`, s7); the unit the loop reads may be a page or a whole document found through a summary embedding (`17-embeddings-and-chunking.md` §3.5). Skeleton: `practices/agent-patterns/agentic-rag-skeleton.py`. **The document form** (s6): the same three tools run over *parsed* documents with provenance — a content field the agent reads as it needs and a metadata field with page and bounding boxes (Abraham, 2026-09, `yt-0I07YAuF8xA…`) — so citations may carry page and bbox, not only file, quote and line; a model-free parser is the fast first pass and the agent is "equip[ped with] a VLM-based parser… as a tool" for a hard page (Liu, 2026-09, `yt-RQi7x-navxU…`, s2 reused; the assistant-loop description is his AI Dev 26 talk, 2026-05, `yt-80vV6fGIlWo…`). For long, organised documents the loop navigates the parsed tree instead of flat chunks — an outline with per-section summaries, open-section tools, "similarity search to find the right document, structure to navigate inside of it" (IBM Technology, 2026-08, `yt-vRZNJWw78BQ…`); the row is in `practices/context-management/context-store-decision.md`, the parsing side in `16-data-for-ai-products.md` §3.4–3.5.

### 3.7 Close the loop, and where to look when it fails

An agent converges only if each iteration injects signal: a test that passes or fails, a checker that answers `OK`/`retry` with reasons, an eval score. Without it "you're just going to have noise" (Schluntz). Verification, not model intelligence, is the limiting factor for real work, because real code rarely has perfect tests — see `05-verification-loops.md`. When an agent fails, the order of suspicion is: the tool (return value, description, bounds), the context (what the model actually saw), the prompt, and only then the model. Do not fine-tune on your own tools: they change daily and the training lag is a bet against frontier capability that, so far, has not paid (Notion). Start with the most capable model to learn the headroom, then optimise cost and latency (`08-model-selection.md`).

## 4. How to apply it in a repo

1. For each LLM feature, write the four answers (complexity, value, critical capabilities, cost of error) in the feature spec; choose workflow / agent / workflow-of-agents explicitly. Template: `practices/agent-patterns/when-to-build-an-agent.md`.
2. Implement the minimal loop first (`agent-loop-skeleton.py` or the equivalent in your framework); no orchestration, no memory, no multi-agent until the single loop passes its eval.
3. Write every tool with `tool-definition-template.md`: UI-shaped return, full description, bounded inputs, errors returned as text, name unique across servers.
4. Decide the transport per tool with `tool-transport-decision-table.md`; record it in `docs/architecture.md`.
5. Before optimising anything, run `prompt-library/trajectory-review.md` on three real trajectories and fix what the model says it was missing.
6. Add the signal: a test, a checker agent with a retry cap, or an eval set of (request → expected tool call); wire it to CI (`05-verification-loops.md`, `practices/verification/`).
7. Re-audit tools monthly with `practices/token-savings/mcp-audit.md`; bucket or add tool search when the count passes ~30.

## 5. Anti-patterns

- Building an agent because the task *could* be an agent, when the decision tree fits on a page.
- One tool per API endpoint; tools without descriptions; parameters named after your schema.
- Raising exceptions inside tools; unbounded reads; no request limit.
- Loading a dozen MCP servers "just in case" and never disabling them.
- Custom formats (XML, JSON DSLs) the model has to be taught, when markdown or SQL would do.
- Adding orchestration, memory or subagents to fix a problem that is a tool bug.
- Optimising cost before the behaviour is right; fine-tuning on tools that will change next week.

## 6. Evidence & sources

- Digest and impact table: `sources/2026-09-24-s12-agents-digest.md` (15 transcripts; log in `sources/2026-09-24-market-scan-s12-intro-to-agents.md`).
- Anthropic, *Building Effective Agents* (2024-12-19); *Writing effective tools for agents* (2025-09-11); Barry Zhang, AI Engineer Summit (2025-03); Erik Schluntz, "Building more effective AI agents" (2025-10-17).
- Mahesh Murag, MCP workshop (2025-03); MCP specification 2026-07-28.
- Notion (Simon Last, Sarah Sachs) on Latent Space (2026-04-15).
- Stanford CME295 Lecture 7 (2025-11-18); Andrew Ng, Sequoia (2024-03-26); Google Cloud Tech ADK (2026-06-10); Dave Ebbelaar (2026-05-10); IBM Technology (2026-08-16, 2026-09-03); Claude, "MCP in Claude Code" (2026-05-09).

## 7. Change log

- 2026-09-24 — created from the session-12 market scan digest. Status `draft` until the LIDR session of 2027-01-14 is ingested and compared.
- 2026-09-27 — reviewed against `sources/2026-09-27-s01-llm-setup-digest.md`; the vendor APIs confirm the loop as the unit of the API (typed items in / typed items out; hosted tools and remote MCP with `allowed_tools` / `require_approval`; "tools are prompts", few tools per server). One refinement to §3.3: besides reading what the model saw, feed its *own reasoning* back into the next turn — OpenAI reports better tool use and lower latency when reasoning items persist across turns. The call itself is now `principles/10-llm-api-fundamentals.md`.
- 2026-09-27 (s2) — refined against `sources/2026-09-27-s02-context-caching-digest.md`: §3.4 gains the addressable-result rule and the fixed-tool-set rule (cache and phantom tools; Manus's three-layer action space). Sub-agents: only the final message crosses the boundary, so it must be self-contained (Chase); default to *communicate* (brief in, structured result out) over *share memory*, which forfeits the cache (Manus); fan out only read-only gathering and converge for anything that must cohere (Cognition vs Anthropic, reconciled). Agentic RAG §3.6 confirmed and refined: a curated manifest (`llms.txt` with good descriptions) plus fetch beat a vector store in Lance Martin's test; leading coding agents do no indexing. Traces: the multi-turn reason ("you don't know what the context at step 14 will be"). Runtime context management itself is `principles/11-runtime-context-management.md`.
- 2026-09-30 (s3) — reviewed against `sources/2026-09-30-s03-wrappers-digest.md`; 12-Factor Agents confirms the minimal-loop stance in its own words (own prompts, context and control flow; tools are JSON + code; stateless reducer; micro-agents inside deterministic code). §3.3 traces now have a standard: the OpenTelemetry GenAI span attributes in `practices/llm-gateway/tracing-otel.md`. No change to the text.
- 2026-10-04 (s7) — reviewed against `sources/2026-10-04-s07-embeddings-chunking-digest.md`: §3.6 confirmed by Lance Martin's CRAG / Self-RAG / adaptive-RAG flows in LangGraph (grade → rewrite or web search → grade hallucination → grade answer; 2024-04) and gains "the unit the loop reads may be a page or document found through a summary embedding" (`17-embeddings-and-chunking.md` §3.5). The flows' depth and the agent-vs-graph trade-off are parked to sessions 9 and 11.
- 2026-10-01 (s6) — refined against `sources/2026-10-01-s06-data-audit-cleaning-privacy-digest.md`: §3.6 gains the document form of agentic RAG — the three tools over parsed documents with provenance (Abraham 2026-09), the model-free parser first and the VLM as a tool (Liu 2026-05), structure navigation for long organised documents (IBM 2026-08); citations may carry page and bbox.
- 2026-10-01 (s5) — reviewed against `sources/2026-10-01-s05-context-memory-permissions-evals-digest.md`: §3.1 question 4 confirmed — scope limits (read-only tools, approvals) are scale limits (Zhang, reused), and the market is moving the other way (write-enabled agents tripled in the Amplify 2026-07 survey, self-report); §3.5 gains Block's permission model for the MCP branch (allow-list by review, destructive annotations with mandatory approval, OAuth via the IdP — Jones 2026-01) and notes the Council demo as MCP sampling in use.
- 2026-10-01 (s4) — reviewed against `sources/2026-10-01-s04-structured-outputs-digest.md`; the minimal-loop stance and "tools are just JSON and code" confirmed (Pokrass; Horthy reused). §3.4 gains one paragraph: a tool call is a structured output dispatched by code; `strict` tool schemas remove hallucinated tool names and malformed arguments; the description-is-prompt rule extends to output schemas (system = when, description = how; descriptive key names are a habit, not officially endorsed).
