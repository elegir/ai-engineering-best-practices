---
title: "Practice — agent entry file (AGENTS.md + CLAUDE.md as a map)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-30
tags: [agents-md, claude-md, rules, cursor]
kind: working-style
applies-when: "always"
reference-status: untested   # untested | field-tested | reference (decision 0005 §3)
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

## Reference implementation

The copyable `AGENTS.md` + `CLAUDE.md` pair in this folder is the reference (text, no code; `reference-status` applies to it all the same — nobody has yet adopted it through this Verify). It is stack-neutral by construction: the only stack-specific lines are the commands it points to, which come from the repo's own `docs/development-guide.md`.

## Stack-sensitive points

- The entry file's *commands* section is the only stack-dependent part: `npm test` / `pytest` / `vendor/bin/pest` / `wp eval`. Point to `docs/development-guide.md` rather than listing them twice.
- Which agent reads which file is tool-dependent, not stack-dependent: Claude Code reads `CLAUDE.md` (and `@imports`), Codex and most others read `AGENTS.md`, Cursor reads `.cursor/rules/*.mdc`. Keep one body and thin pointers.
- WordPress and other repos without a package manifest still need the file; the "install" line then points at the WP-CLI or Docker command the repo already uses.

## Adapt

- Replace every `<<PLACEHOLDER>>` with the repo's real commands and paths; delete lines that do not apply.
- Every prohibition must point to *what enforces it* (a hook in `hooks-and-guards/`, a linter rule, an ADR). A prohibition with no enforcement is a wish — either add the hook or accept it is advisory.
- Keep the root under ~50 lines. If it grows, move the growth into `.claude/rules/<topic>.md` (scoped) or `docs/`.
- The "Shared knowledge base" section is what connects the repo to this KB; keep it.
- Windows: use the `@AGENTS.md` import in `CLAUDE.md`, not a symlink.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

1. The entry file is short enough to be read every session: under sixty lines, and it points to documents instead of restating them — observer: script — negative: a sixty-first line, or a paragraph that duplicates a `docs/` file
2. The agent's own context listing shows the entry file loaded at session start (and the imported companion file, where the agent supports imports) — observer: agent — negative: the file is absent from the loaded context, or only the companion loads
3. Asked "how do I run the end-to-end tests and where are the backend conventions?", the agent answers from the entry file's pointers without exploring the tree — observer: agent — negative: the agent opens test folders or greps for conventions before answering
4. Asked "what must you never do in this repo?", the agent lists every prohibition and names the mechanical hook or rule that enforces each — observer: agent — negative: a prohibition with no mechanism behind it, or a mechanism the entry file does not mention
5. The repo's facts block (decision 0004 §4) is present in the entry file or the file it points to, every fact carries `inferred | planned | asked` and the date — observer: script — negative: a missing block, a fact without a source, or an inferred fact whose evidence no longer exists in the code
6. At session start the agent runs the guard self-test named in the entry file and reports its result in one line — observer: agent — negative: the session proceeds with a guard that did not answer (decision 0005 §6)

**Example commands (Python / Claude Code):** `wc -l AGENTS.md`; `/context` shows `CLAUDE.md` and `AGENTS.md` under Memory files; `python3 .claude/hooks/guard.py --selftest`.

## Sources

- Practitioner guide (≤50 lines, pointer-based), OpenAI (~100-line TOC), Claude Code memory docs (`@import`, rules, `/doctor`) — `sources/2026-09-08-how-teams-structure-agent-knowledge.md`.
- Boris Cherny's shared `CLAUDE.md` ratchet — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2.

## Change log

- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).

- 2026-09-08 — created.
