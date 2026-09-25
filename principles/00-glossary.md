---
title: "Glossary — the vocabulary of building software with AI agents"
type: principle
status: current
date: 2026-09-08
last-reviewed: 2026-09-24
tags: [glossary, vocabulary]
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Glossary

This field renames itself every few months. Below are the terms as used in this knowledge base, each with a plain-language explanation and, where useful, the metaphor that makes it stick. When two sources use different words for the same thing, both are listed.

**Agent (coding agent).** A program that takes a goal in natural language, and then *acts*: reads files, edits them, runs commands, calls tools, checks results, and loops until it decides it is done. Claude Code, Cursor's agent mode, Codex, Copilot's agent, Gemini CLI, OpenCode are all coding agents. Contrast with a *chat assistant*, which only answers.

**Model.** The large language model (LLM) inside the agent — Claude Opus/Sonnet, GPT/Codex, Gemini, etc. The model is rented from a vendor; you cannot change how it thinks, only what you feed it and what surrounds it.

**Harness.** Everything around the model that turns it into a useful agent: the instructions it reads, the tools it can call, the environment it runs in, the state it keeps between steps, and the checks that verify its work. The canonical formula (attributed to Mitchell Hashimoto): **Agent = Model + Harness.** Metaphor from the LIDR workshop: *model = CPU, context = RAM, harness = operating system, agent = the application running on top.* Another: *the model is the engine, the harness is the car.*

**Harness engineering.** The discipline of designing and improving that harness. LIDR's five areas: instructions, tools, local environment, state, feedback. OpenAI's framing: the repository as the agent's system of record, enforced by linters and CI. The practitioner shorthand: *mechanism over prompts.*

**Context.** Everything the model can see when it answers: your prompt, the instruction files, the files it has read, tool outputs, and conversation history. It is finite (the *context window*), and quality degrades as it fills with stale or irrelevant material — that degradation is called **context rot**.

**Context engineering.** Deliberately designing what the agent sees before it acts: project conventions, stack, workflow, constraints, and where to find them. LIDR's "recipe": *technical specifications* + *workflow* (defined by the team) + *the task* (varies), with the golden rule that the context is shared by the whole team. Sits at the base of the pyramid: context → harness → loop.

**Loop engineering.** The top of the pyramid: you no longer trigger the agent; you design the system that triggers it, checks results, and decides what happens next (hooks, CI jobs, scheduled agents, "when X happens run Y"). "The developer stops executing tasks and designs the system that executes them."

**Instruction file** (`CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `copilot-instructions.md`). A Markdown file the agent loads at the start of every session. Best practice: short, pointer-based, a map rather than a manual. `AGENTS.md` is the cross-tool convention; Claude Code reads `CLAUDE.md`, so bridge with `@AGENTS.md`.

**Guides and sensors.** LIDR's split of harness controls by *when* they act. **Guides** act *before* execution: instruction files, linters, constraints, permissions. **Sensors** act *after*: tests, evals, validation, end-to-end checks. A good harness has both.

**Hook.** A shell command or prompt that an agent runtime runs automatically at a lifecycle point — before a tool call (*PreToolUse*: block dangerous commands), after a tool call (*PostToolUse*: run the formatter/linter and feed violations back), when the agent wants to stop (*Stop*: run the tests first), etc. Hooks are *enforced*; instruction files are *suggested*.

**Skill** (`SKILL.md`). A folder packaging procedural knowledge for agents in the Agent Skills open standard: frontmatter (`name`, `description`) + instructions + optional scripts/references. Loaded by **progressive disclosure**: only the name/description at startup, the full file when relevant. Portable across Claude Code, Cursor, Codex, Copilot, and many others.

**Slash command / custom command.** A saved prompt (e.g. `.claude/commands/commit-push-pr.md`) invoked as `/commit-push-pr`. Used for "inner-loop" workflows repeated many times a day.

**Subagent.** A separate agent instance spawned by the main agent for a bounded task (e.g. `code-simplifier`, `verify-app`), with its own context window. Used to keep the main context clean and to parallelize.

**MCP (Model Context Protocol).** An open standard (Anthropic, 2024-11; specification revised 2026-07-28) for exposing capabilities to agents through a server. Three primitives, each with a different *controller*: **tools** (model-controlled — the model decides when to call), **resources** (application-controlled — the app decides what to attach; can be dynamic and subscribable), **prompts** (user-controlled — templates invoked like slash commands). Also *sampling* (a server asks the client for a completion while the client keeps control of model, cost and privacy) and *composability* (a server can itself be a client). An **MCP server** is configured in `.mcp.json` (project scope) or user scope; its tool schemas occupy context even when unused, so audit and disable (`practices/token-savings/mcp-audit.md`). When a CLI exists (`gh`, `aws`, `wp-cli`), coding agents use it more efficiently and can repair it themselves; MCP is the right choice for narrow, tightly-permissioned agents and for publishing a capability to any client. See `principles/21-agent-design-and-tools.md` §3.5.

**Workflow vs agent.** A *workflow* is code that calls the model a fixed number of times in a fixed order (prompt chaining, routing, parallelisation, orchestrator–workers, evaluator–optimiser). An *agent* is a model given tools and an open-ended goal that decides how many steps to take. A *workflow of agents* is a fixed pipeline whose each step is a small closed loop. *Multi-agent* is a parent delegating to sub-agents that run at the same time; to the model a sub-agent is a tool that takes a prompt. Decide with the four-question checklist in `principles/21-agent-design-and-tools.md` §3.1.

**Tool (for a model).** A function the model can call, described by name, description and parameter schema; the description is part of the prompt. Good tools return what a user would see (not one call per API endpoint), return errors as text, are bounded, and use formats the model already knows. **Tool search / router**: a first cheap step that selects the relevant tools from a large catalogue so only their schemas are loaded.

**Spec-driven development (SDD).** Writing a specification (what the change must do, often as user stories or MUST/SHOULD requirements) *before* the agent implements, then verifying the implementation against it. Frameworks: **OpenSpec** (delta specs; lightweight), **Spec-Kit** (GitHub; phased with quality gates and a *constitution*), **Superpowers** (behavioral skills forcing TDD/YAGNI/DRY), **Spec-Boot** (LIDR; the context layer beneath any of them).

**Open spec.** In the workshop's usage: a spec file written as user stories ("As a user, I want to sign up using SSO so that…") kept in the repo as continuous context for the agent. See `templates/open-spec-user-story.md`.

**Delta spec.** OpenSpec's idea: each change describes only what is ADDED / MODIFIED / REMOVED relative to the current spec, so brownfield projects never have to describe the whole system.

**Constitution.** Spec-Kit's name for the document of non-negotiable project rules (architecture, standards, security) that every later phase must respect.

**ADR (Architecture Decision Record).** A short, dated, immutable note recording one decision, its context, and its consequences, with a status (proposed / accepted / superseded / deprecated). Resists rot because an agent can read its status structurally. This KB's `decisions/` folder uses the pattern.

**Definition of done.** The written checklist of what "finished" means for a task (e.g. code + updated docs + unit tests passing + e2e passing + coverage ≥ 90%). If it is written down, the agent can verify itself against it before claiming completion.

**Git worktree.** An additional working directory for the same repository, on its own branch, sharing history. Lets several agent sessions work in parallel without overwriting each other's files. `git worktree add ../proj-feature feature`; Claude Code: `claude --worktree name`; subagents: `isolation: worktree`.

**Plan mode.** An agent mode that reads and proposes but does not edit. Best practice: plan → human approves → execute.

**Eval.** A repeatable test of *agent behavior* (not just code): given this task, does the agent produce an acceptable result? Used in CI to catch regressions in the harness.

**Progressive disclosure.** Loading only metadata first and full content on demand, so many knowledge items can exist without consuming context. The principle behind skills, short entry files, and this KB's `INDEX.md`.

**Single source of truth.** Each fact lives in exactly one file; everything else links to it. Copies drift; links break loudly.

**AI Champion.** (OpenAI Academy / LIDR) The person inside an organization who builds the agentic layer and governs AI adoption so the whole team uses agents with the same criteria — measure → feedback → improve → distribute. Usually the tech lead today.

**Agentic engineer.** An engineer who designs the systems agents execute ("from artisan to manufacturer"). The AI Champion adds the organizational side (influence, change management, training).

**Token.** The unit models are billed and limited by (~¾ of an English word). **Token economy** = the practices that reduce tokens per task: short instruction files, compressed tool output (rtk), code graphs instead of file exploration (codegraph), compacted context (Headroom), terse output (caveman), less over-built code (ponytail), model routing.

**Brownfield / greenfield.** Existing codebase vs. new project. Most real work is brownfield; frameworks that require describing the whole system up front fit it badly.

## Change log

- 2026-09-08 — created from the LIDR workshop and the structuring-research entry.
- 2026-09-24 — MCP entry rewritten with the three primitives and their controllers; added "Workflow vs agent" and "Tool (for a model)"; skills/progressive-disclosure entries reviewed and unchanged. Source: `sources/2026-09-24-s12-agents-digest.md`.
