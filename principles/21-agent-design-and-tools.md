---
title: "Agent design and tools — an agent is a model calling well-designed tools in a loop; decide first whether you need one"
type: principle
status: draft              # draft until LIDR session 12 (2027-01-14) is ingested and compared
date: 2026-09-24
last-reviewed: 2026-09-24
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

### 3.4 Tool design

This is where most of the new knowledge in the scan lives, and where most agent failures live ("99 % of the time it's a bug in one of the tools" — Notion).

- **A tool is one-to-one with your UI, not your API.** If understanding a Slack thread takes three endpoints (conversation, user-id → name, channel-id → name), a model given three tools must make three calls and stitch the result; a person sees it rendered once. Design the tool to return what the person would see, with the surrounding context, in one call. The model is a *user*, not a program.
- **Document tools the way you would for a colleague.** Descriptions and parameter docs are part of the prompt and shape the rest of it. Parameters named `a` and `b` with no docstring fail for the model as they would for an engineer. Put domain hints in the description ("search for the runbook when the user mentions an incident").
- **Give the model formats it already knows.** Notion replaced a lossless custom XML of its block model with a lossy, simple markdown, and a bespoke JSON query language with SQLite — because models know markdown and SQL and had to be prompted into the internal formats. Expose no unnecessary internal complexity.
- **Return errors, do not raise them.** A raised exception ends the loop; a returned human-readable message lets the model read it and correct course. Bound every tool: request limits per run, maximum lines per read, paths confined to an allowed root.
- **Fewer, better tools; disclose progressively.** Vercel's 80 %-fewer-tools case (`02-harness-engineering.md`) is confirmed from every side: models cope with roughly 50–100 tool schemas, quality degrades before the context is full, and any engineer adding a niche tool can make the whole agent worse by over-triggering it. Bucket tools among subagents (~20 each), or add a *tool-search* tool / router that loads full schemas on demand. Avoid name collisions across servers.
- **Describe by goal, not by example.** Notion dropped few-shot examples entirely: modern models instruction-follow well, and goal-driven descriptions let each product team own its tool definition *and its evals* instead of five people guarding one prompt string. If you must tune a description, iterate it with a reasoning model against an eval set of (request → expected tool call) pairs rather than by hand.
- **Verify auth is not the weakest link.** An agent using its own credentials has no notion of the user; OAuth impersonation leaves long-lived tokens on disk; the mature pattern is token exchange (agent authenticated, acting on behalf of the user) with a vault issuing short-lived credentials — detail in the session-14 material. At minimum: know which rung of that ladder each tool is on.

Template and checklist: `practices/agent-patterns/tool-definition-template.md`.

### 3.5 How to expose tools: CLI, MCP, skill, RAG, memory

MCP standardises three primitives, each with a different controller: **tools** (the model decides when to call), **resources** (the application decides what to attach; can be dynamic and subscribable), **prompts** (the user invokes them, like slash commands); plus *sampling* (a server asks the client for a completion while the client keeps control of model, cost and privacy) and *composability* (a server can itself be a client, so agents chain). Roadmap items from the March 2025 launch talk — remote servers with OAuth, the registry, `.well-known` discovery, tool annotations such as read-vs-write, namespacing — are in the 2026-07-28 specification; go to the spec, not the talk, for what exists.

The 2026 debate is not whether MCP works but when to use it. Notion's Simon Last, after five harness rebuilds: **CLIs** are better for coding agents — they run in the terminal (pagination, cursors), give progressive disclosure for free (`--help`), and are *bootstrapped*: the agent can debug and fix its own tool in the same environment, whereas a broken MCP transport leaves the agent with nothing. **MCP** is better for a narrow, lightweight agent without a compute runtime and when a tight permission model matters ("all you can do is call the tools"; a CLI raises real questions about token exfiltration). It is also wasteful to pay a model to renegotiate a deterministic integration on every call. Claude's own guidance agrees operationally: MCP tool definitions sit in context even unused, so disable what you do not use, prefer a CLI (`gh`, `aws`, `wp-cli`) where one exists, and package CLI usage as a **skill** so the instructions load only when relevant. IBM's rule of thumb completes the picture: knowledge someone *wrote down* → RAG; knowledge the agent *learned from experience* → memory; a repeatable *procedure* with judgment about when to escalate → skill; reaching *out into the world* → MCP. Decision table: `practices/agent-patterns/tool-transport-decision-table.md`.

Whatever you choose, keep one internal abstraction (`tool`, `agent`, `completion`, `integration`) so that MCP is one integration type among others and the framework can be replaced; every team that has shipped at scale has rebuilt theirs several times.

### 3.6 Agentic RAG

Classic semantic RAG (embed → retrieve → one LLM call) is not dead: it wins on latency and cost. Agentic RAG wins on quality because the loop can self-correct when the first search misses. The minimal, framework-free version is three tools over a folder of markdown — `list_files`, `grep` (ripgrep), `read_file` with a line cap — and a structured output with citations (file, quote, line). These are exactly the primitives coding agents use over a codebase; the same loop works over a Postgres table of documents. The framework version (LangGraph) adds a *grade documents* step and a *rewrite query* branch. Skeleton: `practices/agent-patterns/agentic-rag-skeleton.py`.

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
