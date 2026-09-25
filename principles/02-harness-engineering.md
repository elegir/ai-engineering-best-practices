---
title: "Harness engineering — building the environment that makes an agent reliable"
type: principle
status: current
date: 2026-09-08
last-reviewed: 2026-09-24
tags: [harness-engineering, tools, sandbox, state, feedback]
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Harness engineering

## 1. The question this answers

Once the agent knows the project (context), what else must exist around it so that it can work autonomously, safely, and verifiably — and so that the whole setup gets better every time something goes wrong?

## 2. Short answer

Build and maintain five things: **instructions** (context + entry file), **tools** (CLI, files, git, MCPs), a **local environment** the agent can actually run, **persisted state** so work survives session boundaries and hand-offs, and **feedback** (linters, builds, tests, e2e, evals) that verifies output *and* feeds improvements back into the harness. Prefer mechanical enforcement (hooks, linters, CI) over more prose. Treat every agent failure as a reason to add a control, not to fix by hand. The model is almost never the problem.

## 3. Long explanation

### The formula and the evidence

**Agent = Model + Harness.** The model supplies intelligence; the harness supplies the context it receives, the rules it respects, the tools it can reach, the tests and evals that verify what it produces, the sandbox it runs in, and the observability to know what it decided and why. The cases every source repeats: Vercel cut 80% of its text-to-SQL agent's tools and success went from 80% to 100% (3.5× faster, 37% fewer tokens); LangChain moved its coding agent from #30 to #5 on Terminal-Bench 2.0 without touching the model; Stripe merges ~1,300 agent-written PRs a week with humans only reviewing; Microsoft's Azure SRE Agent went from 100+ specialized tools to filesystem-based context and raised "intent met" on novel incidents from 45% to 75%. The practitioner guide cites a same-model comparison where swapping the harness moved SWE-bench by 22 points and swapping the model by 1. And as models improve, harness design matters *more*, because stronger models expose bottlenecks weaker ones masked.

### The five areas (LIDR) and the six primitives (LangChain/LIDR)

LIDR's kitchen model — the robot in a kitchen needs a recipe book, knives, a stove, a prep table, and a chef who tastes the dish — maps to:

1. **Instructions**: `CLAUDE.md`/`AGENTS.md` *plus* the technical docs inside the repo (see `01-context-engineering.md`); MCPs for context that must stay external (Jira, Confluence, Notion).
2. **Tools**: terminal, file system, git, MCP servers. Note the Vercel lesson: *fewer, better tools* beat many. Remove tools that prove irrelevant. How to design a tool the model can actually use — UI-shaped returns, documented like a function, errors returned as text, bounded — is in `principles/21-agent-design-and-tools.md` §3.4 and `practices/agent-patterns/tool-definition-template.md`.
3. **Local environment**: pinned dependencies and versions, services that can be launched, written instructions for running tests, starting the DB, and bringing up the whole stack. Without it the agent cannot verify and cannot be autonomous.
4. **State**: a persisted task artifact recording where work stands, so a session can be resumed after a cut, a reboot, or a hand-off to another agent, and so work can be split across agents. The practitioner guide adds: standardize the startup routine (check directory, read `git log --oneline -20` and the progress file, pick the next task, sanity-check the dev server); prefer JSON for progress files.
5. **Feedback**: linter, build, unit tests, e2e (Playwright/Cypress), API collections (Postman/Hurl) → pass means commit/PR, fail means correct. *And* feedback improves the harness: change instructions, add or remove tools, fix the environment config.

The complementary list of **primitives** any harness has: filesystem (durable state), code execution (a terminal is a general-purpose computer), sandbox (act without breaking production), memory & search (project instructions, web, vector KBs), context management (compaction and offloading against context rot), and **guides + sensors** (before vs after execution).

### Mechanism over prompts

"Remember to write tests" in an instruction file is a suggestion; a Stop hook that runs the tests is a fact. The practitioner guide's ordering: push every check to the fastest layer that can hold it — PostToolUse hook (milliseconds) → pre-commit hook (seconds) → CI (minutes) → human review (hours). Four hook patterns for Claude Code:

- **Safety gates (PreToolUse)**: block destructive commands (`rm -rf`, `DROP TABLE`, `terraform apply` on prod), protect sensitive files (`.env`) and *linter configs* (so the agent cannot silence a rule instead of fixing code); exit code 2 sends the reason back to the agent. Ban `git commit --no-verify`.
- **Quality loops (PostToolUse)**: after every Write/Edit, auto-format, then lint and return remaining violations as structured JSON in `hookSpecificOutput.additionalContext` so the agent self-corrects. Use fast Rust-based tools (Biome/Oxlint for TS, Ruff for Python, gofumpt/golangci-lint for Go, rustfmt/clippy for Rust) because the loop must finish in milliseconds.
- **Completion gates (Stop)**: tests must pass before the agent may declare done; check the `stop_hook_active` flag to avoid infinite loops.
- **Observability**: stream intent, results and context-loss events somewhere you can inspect.

Write linter error messages as **fix instructions** (`ERROR / WHY (link to ADR) / FIX / EXAMPLE bad→good`), because agents cannot ignore a CI failure but can ignore documentation. Pair architectural decisions with executable rules (the "archgate" pattern). Constrain the solution space — fixed layers with validated dependency direction, cross-cutting concerns through one interface — and paradoxically trust in agent output *rises*.

### The ratchet

Boris Cherny: "Every time we see Claude do something incorrectly, we add it to `CLAUDE.md`." LIDR: when an agent fails, design a control that prevents recurrence. The practitioner guide: add a test or linter rule every time the agent makes a mistake. OpenAI: encode "golden principles" and run background garbage-collection agents that open small corrective PRs. Same idea at four scales. The harness compounds; manual fixes do not.

### Skills, commands, subagents, loops

On top of docs and the entry file: **skills** for anything repeatable (a `commit` skill that encodes how a commit is made; a code-audit skill run before finishing), **slash commands** for inner-loop workflows done dozens of times a day (`/commit-push-pr` with inline bash pre-computing git state), **subagents** for bounded recurring jobs (`code-simplifier` after work, `verify-app` for e2e), and then **loops**: "when I ask for a commit, run the audit first"; "when the agent finishes, a background agent verifies"; eventually a full user-story-to-commit pipeline. Start manual; automate only what is proven.

### Permissions

Do not run with permissions disabled on your real machine. Pre-allow known-safe commands via `/permissions` and commit them in `.claude/settings.json`. Relax permissions only inside a sandbox (container, cloud session, worktree with an isolated DB).

## 4. How to apply it in a repo

1. Confirm the environment works from the agent's seat: can it install, start the stack, seed the DB, run unit + integration + e2e tests from written instructions alone? Fix that first.
2. Write a `progress`/task-state file the agent reads at session start and updates at session end; standardize the startup routine in the entry file.
3. Add hooks in this order: PostToolUse formatter → PreToolUse protection of `.env` and linter configs → Stop hook running the test suite.
4. Audit tools/MCPs: remove ones never used; keep the ones that give context the repo cannot hold (DB access, browser, error tracker).
5. Turn the two or three most repeated workflows into slash commands or skills.
6. Keep a "harness changelog": every time the agent errs, record what control was added (rule, test, hook, doc line).
7. Only then consider loops and parallel agents (`06-parallel-agents-and-worktrees.md`).

## 5. Anti-patterns

- Prompt-only enforcement.
- Many tools "just in case" (Vercel's lesson).
- Scaling to many agents before one agent works reliably — that creates compounding cognitive debt.
- Agent-only infrastructure. Build excellent developer infrastructure; agents benefit automatically (Stripe).
- Letting the agent edit linter configs or bypass hooks.
- Fixing agent mistakes by hand without adding a control.

## 6. Evidence & sources

- LIDR workshop hub §4 and video B — `sources/2026-09-08-lidr-workshop-harness-engineering.md` (§3.4, §3.9).
- Practitioner guide (hooks, MVH roadmap, anti-patterns), OpenAI, awesome-harness-engineering — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` (§3.1–3.3, §3.8).
- Boris Cherny's setup — workshop entry §3.2.

## 7. Change log

- 2026-09-08 — created.
- 2026-09-24 — reviewed against `sources/2026-09-24-s12-agents-digest.md`. Confirmed: Agent = Model + Harness ("environment + tools + system prompt, model in a loop" — Zhang), "the model is almost never the problem" ("99 % of the time it's a tool bug" — Notion), keep it simple, fresh-context loops over a progress file for long tasks (the mainstream 2026 "harness" narrative matches `practices/session-state/`). Added a pointer from the Tools area to principle 21 and the tool-definition template; no other change.
