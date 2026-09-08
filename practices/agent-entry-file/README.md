---
title: "Practice — agent entry file (AGENTS.md + CLAUDE.md as a map)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [agents-md, claude-md, rules, cursor]
principle: principles/03-agent-instruction-files.md
sources:
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
supersedes: null
superseded-by: null
---

# Agent entry file

## Solves

The repo has no instruction file, or it has one that is hundreds of lines of description, contradicts itself, or duplicates what the code already says. Symptoms: the agent ignores rules that are in the file; it asks how to run tests; it does not know where the docs are; each tool (Claude Code, Cursor, Codex) has a different, drifting set of rules.

## Applies when

- Any repo an agent works in more than once.
- Especially when `context-docs-skeleton/` exists — the entry file is what points to it.

## Does not apply when

- Nothing; even a script folder benefits from a 10-line `AGENTS.md`. Scale the content down, not the practice.

## Files in this folder

| File | Copy to | Purpose |
|---|---|---|
| `AGENTS.md` | `<repo>/AGENTS.md` | The canonical, cross-tool entry file (~50 lines) |
| `CLAUDE.md` | `<repo>/CLAUDE.md` | Imports `AGENTS.md`; Claude-specific lines only |
| `CLAUDE.local.md.example` | `<repo>/CLAUDE.local.md` (gitignored) | Personal notes that must not be committed |
| `dot-claude/rules/api.md` | `<repo>/.claude/rules/<topic>.md` | Example of a path-scoped rule that loads only when matching files are touched |
| `.cursor-rules-pointer.mdc` | `<repo>/.cursor/rules/00-agents.mdc` | Makes Cursor read the same `AGENTS.md` |

## Adapt

- Replace every `<<PLACEHOLDER>>` with the repo's real commands and paths; delete lines that do not apply.
- Every prohibition must point to *what enforces it* (a hook in `hooks-and-guards/`, a linter rule, an ADR). A prohibition with no enforcement is a wish — either add the hook or accept it is advisory.
- Keep the root under ~50 lines. If it grows, move the growth into `.claude/rules/<topic>.md` (scoped) or `docs/`.
- The "Shared knowledge base" section is what connects the repo to this KB; keep it.
- Windows: use the `@AGENTS.md` import in `CLAUDE.md`, not a symlink.

## Verify

1. `wc -l AGENTS.md` ≤ ~60.
2. In Claude Code run `/context` — `CLAUDE.md` and `AGENTS.md` (via import) appear under Memory files.
3. Ask the agent "how do I run the e2e tests and where are the backend conventions?" — it answers from the file without exploring.
4. Ask "what must you never do in this repo?" — it lists the prohibitions and names the hook/rule behind each.

## Sources

- Practitioner guide (≤50 lines, pointer-based), OpenAI (~100-line TOC), Claude Code memory docs (`@import`, rules, `/doctor`) — `sources/2026-09-08-how-teams-structure-agent-knowledge.md`.
- Boris Cherny's shared `CLAUDE.md` ratchet — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2.

## Change log

- 2026-09-08 — created.
