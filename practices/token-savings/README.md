---
title: "Practice — token savings (measure, then cut in order)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-30
tags: [tokens, rtk, codegraph, mcp-audit, model-routing]
kind: working-style
applies-when: "always"
reference-status: untested   # untested | field-tested | reference (decision 0005 §3)
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

## Reference implementation

`checklist.md`, `mcp-audit.md`, `measurement-log.md`. Documents only; the contract is about numbers recorded, not about any file format.

## Stack-sensitive points

- Tool schema cost depends on which MCP servers the repo loads, not on the product's language.
- Verbose build or test output is the main per-stack difference: `pytest -q`, `npm test -- --silent`, `vendor/bin/pest --compact`, WP-CLI `--quiet`; put the quiet flag in `hooks.json` once.

## Adapt

- Do the free steps first (context docs, short entry file, tool audit); install tools one at a time, a week each.
- Windows: `rtk` and `codegraph` install notes are in `checklist.md`; check each project's README for the current install method — these tools move fast.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

1. `measurement-log.md` has a baseline row and one row per change, each with a number (tokens or cost per session or per task), not an impression — observer: Martin — negative: a change with no number
2. At session start, instruction files and tool schemas together occupy well under half the context window — observer: agent — negative: a session that starts above half
3. Every MCP server or tool set loaded at startup is used in the last month, per `mcp-audit.md`; unused ones are disabled — observer: Martin — negative: a loaded server with no use
4. Long tool outputs are truncated or summarised before entering context, and the raw output is kept on disk for the agent to read on demand — observer: agent — negative: a thousand-line log pasted into the conversation

**Example commands (Claude Code):** `/context`; the audit table in `mcp-audit.md`.

## Sources

- LIDR §5 tools and numbers (each tool's own claims); Vercel tool-pruning case; Claude Code MCP tool search; accessibility tree vs screenshots — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.5; `sources/2026-09-08-how-teams-structure-agent-knowledge.md` §3.2–3.3.

## Change log

- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).

- 2026-09-08 — created.
