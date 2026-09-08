---
title: "Token economy — spend fewer tokens per task without losing quality"
type: principle
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [tokens, cost, context-management, rtk, codegraph]
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Token economy

## 1. The question this answers

Martin hits his plan's weekly token limits. What actually reduces tokens per task, in what order should it be tried, and what should *not* be sacrificed?

## 2. Short answer

Most waste comes from four things: the agent re-exploring the repo every request, bulky tool output (terminal, logs, test runs) entering context, over-long instruction files and over-broad tool/MCP sets, and using the top model for routine work. Fix in this order: (1) good context so the agent reads the docs instead of exploring; (2) short pointer-style entry file and fewer tools; (3) compress terminal output (`rtk`) and context (`Headroom`); (4) query a code graph instead of walking files (`codegraph`); (5) route routine tasks to the mid-tier model; (6) trim agent verbosity (`caveman`) and over-built code (`ponytail`). Never save tokens by skipping verification.

## 3. Long explanation

### Where the tokens go

Every session starts by loading instruction files, rules, and skill metadata; every tool call adds its schema; every command adds its output; every file the agent reads to "understand the codebase" adds its content; and every turn re-sends the growing context. A large `CLAUDE.md` plus a dozen MCPs plus a verbose test run can consume most of a window before real work starts. Context rot then degrades quality, and the agent compensates by reading more — a spiral.

### The levers, with the workshop's numbers (each tool's own claims)

1. **Context first.** With `docs/` in place the agent reads `testing-standards.md` instead of ten test files. This is the largest and least-discussed saving.
2. **Shorter instructions, fewer tools.** Vercel: removing 80% of tools cut tokens 37% and raised success. Claude Code's MCP Tool Search loads tool schemas on demand (up to ~85% less context per the practitioner guide).
3. **rtk** — compresses terminal output before the model sees it; 60–90% fewer tokens on common commands. Easiest install; first thing to try. github.com/rtk-ai/rtk
4. **Headroom** — compresses context (logs, test output) before it counts as input; up to 95% per its docs. github.com/headroomlabs-ai/headroom
5. **codegraph** — a local code graph the agent queries instead of exploring file by file; ~57% fewer tokens on average. github.com/colbymchenry/codegraph
6. **Model routing** — top tier for planning/architecture/deep debugging, mid tier for routine implementation (`08-model-selection.md`); Cursor/Copilot "Auto" modes; OpenRouter or LiteLLM at API level.
7. **caveman** — terser agent responses; ~65% fewer output tokens. github.com/JuliusBrussee/caveman
8. **ponytail** — targets over-built code the agent *writes*; up to 80–94% less in over-construction cases. github.com/DietrichGebert/ponytail
9. **Structured over visual** — accessibility trees and JSON instead of screenshots for browser verification (4–20× cheaper per the practitioner guide's measurements).
10. **Compaction discipline** — use a PreCompact hook to protect important state; keep the progress file outside the conversation so compaction loses nothing that matters.

Álvaro Moya reports ~60% personal savings combining these ("my experience, not a benchmark"). Local models (Qwen, Kimi, GLM) for well-defined tasks are a trend to watch, not a recommendation yet; re-verify versions before adopting.

### What not to cut

Verification. A skipped e2e run saves tokens once and costs a production incident. The Faros data in the workshop (bugs +54%, incidents per PR +243%) is what "fast and unverified" looks like at scale.

## 4. How to apply it in a repo

1. Measure: note weekly usage before changes; keep a one-line log per experiment.
2. Do `01-context-engineering.md` and `03-agent-instruction-files.md` first.
3. Install `rtk`; use it for a week; record the delta.
4. Audit MCPs and tools; remove the unused; enable tool search.
5. Try `codegraph` on the largest repo.
6. Set a model policy: plan with the top tier, execute with the mid tier.
7. Only then try `caveman`/`ponytail`/`Headroom`; each one for a week, measured.

## 5. Anti-patterns

- Saving tokens by disabling tests or e2e.
- Trimming the instruction file by deleting prohibitions that prevent expensive mistakes.
- Adding five compression tools at once — no way to know which helped.
- Using the top model for everything by default (the opposite of Cherny's choice, which he justifies by *less steering*; measure which is cheaper for you).

## 6. Evidence & sources

- LIDR hub §5 and the token-saving article — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.5.
- Vercel case; MCP tool search; accessibility-tree token counts — `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.2–3.3.

## 7. Change log

- 2026-09-08 — created.
