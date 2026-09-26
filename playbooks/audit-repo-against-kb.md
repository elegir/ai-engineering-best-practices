---
title: "Playbook — audit a repository against the knowledge base and propose a plan"
type: playbook
status: current
date: 2026-09-08
last-reviewed: 2026-09-26
tags: [audit, adoption, harness, context]
sources:
  - principles/01-context-engineering.md
  - principles/02-harness-engineering.md
  - principles/03-agent-instruction-files.md
  - principles/05-verification-loops.md
supersedes: null
superseded-by: null
---

# Audit a repository against the knowledge base

**Who runs this.** An agent, inside the target repository, on Martin's request.

**Output.** One Markdown file, `docs/kb-audit-YYYY-MM-DD.md` in the target repo (or printed to chat if the repo has no `docs/`), containing findings and a prioritized plan. **No other files are changed by this playbook.** Implementation happens only after Martin approves, one item per prompt.

**Rules.** Investigation before implementation. Reference actual files, commands and gaps in *this* repo — no generic advice. Explain each finding simply, assuming the reader may not know the term; link the principle. Prefer mechanical fixes (hooks, linters, tests) over prose additions. When unsure, ask one question at a time.

## Step 0 — Which practices apply

Run `playbooks/which-practices-apply.md` first (facts with evidence → one confirmation screen → applies / skipped with reasons). Audit only the practices it marked *applies* or *already present*; list the *skipped* ones at the end of the report with their reasons so the omission is visible.

## Step 1 — Inventory (read only)

Collect and list:

- Entry files: `CLAUDE.md`, `AGENTS.md`, `CLAUDE.local.md`, `.claude/rules/`, `.cursor/rules/`, `.cursorrules`, `.github/copilot-instructions.md`. Line count of each.
- Docs: `README*`, `docs/**`, any `*-standards.md`, `data-model*`, `api-spec*`, `openapi*`, `workflow*`.
- Harness: `.claude/settings*.json` (hooks, permissions), `.claude/commands/`, `.claude/agents/`, `skills/` or `.claude/skills/`, `.mcp.json` / `mcp.json`, `lefthook.yml` / `.pre-commit-config.yaml`, CI config.
- Environment: how to install, start the stack, seed data, run unit/integration/e2e tests — from written instructions only. Note anything that requires tribal knowledge.
- State: any progress/task file the agent reads at start; `git log --oneline -20` for recent history.
- Sensors: formatter, linter, type checker, unit, integration, e2e tooling; coverage config; what runs automatically vs by hand.
- Parallelism: worktrees in use, `.worktreeinclude`, per-worktree DB/port handling.
- Specs: any spec/user-story files; OpenSpec/Spec-Kit presence.
- Token hygiene: number of MCPs/tools configured; size of instruction files; `rtk`/`codegraph` presence.

## Step 2 — Score against the principles

For each row, mark **Present / Partial / Missing** and cite the file or the absence.

| Area | Principle (why) | Practice (how — copy from) | Check |
|---|---|---|---|
| Context: technical specs | `01-context-engineering.md` | `practices/context-docs-skeleton/` | stack, dev guide, architecture, data model (+Mermaid), per-layer standards, API contract exist as separate docs |
| Context: workflow & DoD | `01-context-engineering.md` | `practices/context-docs-skeleton/docs/workflow.md`, `practices/verification/definition-of-done.md` | workflow doc with phases, roles, deliverables, definition of done (TDD, coverage, e2e, docs update) |
| Entry file | `03-agent-instruction-files.md` | `practices/agent-entry-file/` | ≤ ~50 lines root (hard limit 200), pointer-based, commands + prohibitions + docs map; `CLAUDE.md` imports `AGENTS.md` |
| Environment | `02-harness-engineering.md` | `practices/context-docs-skeleton/docs/development-guide.md` | agent can bring up the stack and run all test layers from written instructions |
| Tools/MCPs | `02-harness-engineering.md` | `practices/token-savings/mcp-audit.md` | only tools actually used; DB/browser/error-tracker access where needed |
| State | `02-harness-engineering.md` | `practices/session-state/` | progress file + startup routine |
| Sensors | `05-verification-loops.md` | `practices/verification/` + `practices/hooks-and-guards/` | formatter/linter (PostToolUse), unit (pre-commit), e2e (Stop/CI), configs protected, `--no-verify` banned |
| Specs | `04-spec-driven-development.md` | `practices/spec-driven/`, `templates/open-spec-user-story.md` | spec-before-code practice; open specs as user stories; framework if any |
| Prompts/commands | `01`, `04` | `practices/prompt-library/` | ask-the-expert, audit, lesson→rule, commit skill available as commands |
| Worktrees | `06-parallel-agents-and-worktrees.md` | `practices/worktrees/` | worktree per ticket, `.worktreeinclude`, infra isolation |
| Tokens | `07-token-economy.md` | `practices/token-savings/` | instruction size, tool count, compression tools, measurement log |
| Model policy | `08-model-selection.md` | `practices/context-docs-skeleton/docs/workflow.md` §3 | plan-high/execute-mid documented |
| Agents & tools (only if `tools or multi_agent`) | `21-agent-design-and-tools.md` | `practices/agent-patterns/` | workflow-vs-agent decision recorded; tools pass the 12-point checklist; transport chosen; a signal closes the loop |

## Step 3 — Findings

For every Partial/Missing: one paragraph — what is missing, why it matters *for this repo* (name a real recent failure or risk if `git log` or issues show one), which principle, **which practice folder provides the files**, whether its `applies-when` line holds for this repo (quote the facts and their evidence from Step 0), which stack variant fits, and the smallest mechanical fix.

## Step 4 — Plan

Order by: (1) things that block the agent from verifying its work (environment, sensors → `verification/`), (2) context docs (`context-docs-skeleton/`), (3) entry-file cleanup (`agent-entry-file/`), (4) hooks (`hooks-and-guards/`), (5) state (`session-state/`), (6) prompts/commands (`prompt-library/`), (7) specs (`spec-driven/`), (8) worktrees, (9) token savings. Each item: title, practice folder + variant, files to copy and where, placeholders to fill, effort (S/M/L), done-when (the practice's Verify section). Keep it to the top 7. Append "later" items separately.

## Step 5 — Stop

Present the plan. Wait for Martin's approval. Then execute **one item per prompt**: copy the practice's files, replace every `<<PLACEHOLDER>>`, adapt per its "Adapt" section, run its "Verify" section, and add a one-line entry to the repo's `docs/harness-changelog.md` (`YYYY-MM-DD — adopted practices/<name> (<variant>)`).
