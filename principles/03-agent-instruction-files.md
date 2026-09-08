---
title: "Agent instruction files — CLAUDE.md / AGENTS.md as a map, not a manual"
type: principle
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [claude-md, agents-md, instruction-files, cursor-rules]
sources:
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
supersedes: null
superseded-by: null
---

# Agent instruction files

## 1. The question this answers

What should go in `CLAUDE.md` / `AGENTS.md` (and Cursor rules, Copilot instructions), how long should it be, and how do several tools share one set of instructions?

## 2. Short answer

Keep the root file **short (aim for ~50 lines; never past 200) and pointer-based**: build/test/run commands, hard prohibitions (each pointing at a rule, ADR or hook), the startup routine, and *where* the deep documents live. Put everything else in `docs/`, path-scoped rules, or skills that load on demand. Maintain one `AGENTS.md` for all tools and make `CLAUDE.md` import it (`@AGENTS.md`). Grow it by the ratchet: every repeated mistake earns one line — and every line must answer "would removing this cause mistakes?"

## 3. Long explanation

### Why short

Instruction files are loaded into every session, so they consume context before the first question, and adherence drops as instruction count grows — the practitioner guide reports primacy bias becoming pronounced around 150–200 instructions, and files over 1,000 lines that "burn context before the first question". Anthropic's own guidance targets under 200 lines and says shorter produces better adherence. OpenAI keeps `AGENTS.md` at ~100 lines as a table of contents into `docs/`. Boris Cherny's team runs on one shared `CLAUDE.md` that the whole team edits several times a week — small, alive, and committed.

### Why pointers

A pointer ("ADRs live in `docs/adr/`; run `archgate check` to verify architecture rules") fails loudly when it breaks — the path 404s. A description ("our architecture has three layers…") rots silently. Agents can also *read* `package.json`, `pyproject.toml`, the directory tree; describing them wastes lines. What they cannot derive is the tribal knowledge: pitfalls, rationale, conventions that differ from tool defaults, and where the standards documents are.

### What goes in (root file)

- The three to six commands that matter: install, run, test, lint, e2e, deploy-to-staging.
- The startup routine: read the progress file, check `git log`, pick the next task.
- Prohibitions, each with a pointer: "never edit `.env` (PreToolUse hook enforces)", "never `--no-verify`", "never merge without e2e passing (see `docs/workflow.md`)".
- Map of `docs/`: one line per document with when to read it.
- Pointers to skills/commands and to shared knowledge (this KB).
- Tool-specific notes in a short section under the import (e.g. "use plan mode for changes under `src/billing/`").

### What stays out

- System-state prose (architecture narratives, API descriptions) — put in `docs/` and keep it updated by the workflow, or replace with generated artifacts.
- Tech-stack lists — derivable.
- Long style guides — delegate to linters/formatters; the entry file only says which command runs them.
- Multi-step procedures — those are skills.
- Anything that applies to only one part of the tree — that is a path-scoped rule.

### Layering (Claude Code specifics, similar elsewhere)

- Hierarchy: managed policy → `~/.claude/CLAUDE.md` (personal, all projects) → `./CLAUDE.md` (project, committed) → `./CLAUDE.local.md` (personal, gitignored). Files above the working directory load at launch; files in subdirectories load when Claude reads files there.
- `.claude/rules/*.md`: one topic per file; add `paths:` frontmatter to load a rule only when matching files are touched (e.g. API rules only for `src/api/**`). This is how you keep the root short without losing detail.
- `@path` imports pull other files in **at launch** (they still cost context; relative to the importing file; depth ≤ 4). Use them for `@AGENTS.md`, not for bulk.
- Skills load only when relevant — the right home for procedures.
- `/doctor` proposes trims for a checked-in `CLAUDE.md`; `/context` shows which memory files actually loaded; `/init` reads Cursor/Copilot rules and can seed a `CLAUDE.md` (and with the new init flow, `AGENTS.md`, Windsurf, Cline rules too).
- Block-level HTML comments are stripped before injection — use them for maintainer notes that should not cost tokens.

### One file for all tools

`AGENTS.md` is the cross-tool convention (Codex, Cursor, Copilot, Gemini CLI, OpenCode… read it). Claude Code reads `CLAUDE.md`. Bridge with:

```markdown
@AGENTS.md

## Claude Code
- Use plan mode for changes under `src/billing/`.
```

On Windows use the import, not a symlink (symlinks need admin or Developer Mode). Spec-Boot (LIDR) does the same job with symlinks so every copilot reads the same `docs/`.

### The ratchet, applied to this file

Add a line when: the agent makes the same mistake twice; a code review catches something it should have known; you type the same correction you typed last session; a new teammate would need it. During PR review, tag the agent to add the lesson to `CLAUDE.md` *as part of the PR* (Cherny's "compounding engineering"). Remove a line when it stops earning its place.

## 4. How to apply it in a repo

1. Read the current file(s). Count lines. Mark each line: command / prohibition / pointer / derivable / system-state prose / procedure / scoped.
2. Move derivable and prose lines to `docs/` (or delete); procedures to `skills/`; scoped lines to `.claude/rules/<topic>.md` with `paths:`.
3. Rewrite the root as: commands → startup routine → prohibitions with pointers → docs map → shared KB pointer. Target ~50 lines.
4. Create `AGENTS.md` as the canonical file and `CLAUDE.md` = `@AGENTS.md` + a short Claude section.
5. Run `/context` in a session to confirm what loaded; run `/doctor` for trim suggestions.
6. Test with one real task; if the agent asks for something the file should have pointed to, add the pointer.

## 5. Anti-patterns

- The 1,000-line `CLAUDE.md` that is really the standards document.
- Contradictory instructions across root, nested files and rules — the agent picks one arbitrarily. Review periodically.
- Instructions that are really enforcement needs ("never do X") without a hook behind them.
- Duplicating `AGENTS.md` into `CLAUDE.md` instead of importing.
- Personal preferences in the committed file (use `CLAUDE.local.md` or `~/.claude/CLAUDE.md`).

## 6. Evidence & sources

- Practitioner guide §3 "pointer-based"; OpenAI ~100-line TOC; Claude Code memory docs — `sources/2026-09-08-how-teams-structure-agent-knowledge.md`.
- Boris Cherny's shared `CLAUDE.md`; LIDR's "instructions" area — `sources/2026-09-08-lidr-workshop-harness-engineering.md` (§3.2, §3.9 video B).

## 7. Change log

- 2026-09-08 — created.
