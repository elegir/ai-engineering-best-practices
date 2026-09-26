---
title: "Practice — token savings (measure, then cut in order)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-24
tags: [tokens, rtk, codegraph, mcp-audit, model-routing]
kind: working-style
applies-when: "always"
principle: principles/07-token-economy.md
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
supersedes: null
superseded-by: null
---

# Token savings

## Solves

Weekly token limits get hit; sessions slow down as context fills; the agent re-reads the repo on every task. This practice is an ordered checklist with the exact installs, plus a measurement log so you know which change actually helped.

## Applies when

- Any repo where you hit limits or sessions feel sluggish after 20 minutes.

## Does not apply when

- Never skip verification to save tokens. If a step here would remove a sensor, it is the wrong step.

## Files in this folder

| File | Purpose |
|---|---|
| `checklist.md` | The ordered steps with install commands and what to expect |
| `mcp-audit.md` | Template to list every MCP/tool, its usage in the last 2 weeks, and keep/remove |
| `measurement-log.md` | One line per experiment: before/after, kept or reverted |

## Adapt

- Do the free steps first (context docs, short entry file, tool audit); install tools one at a time, a week each.
- Windows: `rtk` and `codegraph` install notes are in `checklist.md`; check each project's README for the current install method — these tools move fast.

## Verify

- `measurement-log.md` has a baseline row and one row per change with a number, not an impression.
- `/context` in Claude Code shows the instruction files and tool schemas well under half the window at session start.

## Sources

- LIDR §5 tools and numbers (each tool's own claims); Vercel tool-pruning case; Claude Code MCP tool search; accessibility tree vs screenshots — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.5; `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.2–3.3.

## Change log
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).

- 2026-09-08 — created.
