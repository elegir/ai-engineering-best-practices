---
title: "Practice — prompt library (the prompts that generate context and discipline)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [prompts, meta-prompt, ask-the-expert, commands, skills]
principle: principles/01-context-engineering.md
sources:
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
supersedes: null
superseded-by: null
---

# Prompt library

## Solves

The same high-leverage prompts get reinvented, badly, in every session, so quality depends on who is typing. The workshop's point: daily prompts should be one-liners; the *good* prompts are the ones that **create context** (docs, specs, tests) and **enforce discipline** (audit before commit). Keep them as files an agent can run as commands.

## Applies when

- Any repo. Copy the ones that fit; delete the rest.

## Does not apply when

- Never fully — even a docs repo benefits from `ask-the-expert` and `code-audit` (as a doc audit).

## Files in this folder

| File | Use as | Purpose |
|---|---|---|
| `meta-prompt.md` | `/meta` command or paste | Turns a one-line request into a structured ROLE/CONTEXT/OBJECTIVE/REQUIREMENTS/FORMAT/QUALITY prompt |
| `ask-the-expert.md` | `/ask-expert` | Forces clarification questions before any design or implementation |
| `readme-by-index.md` | paste | One-shot template: fill a fixed index, never invent structure |
| `openapi-from-code.md` | paste | Generate/refresh `docs/api-spec.yml` |
| `standards-document.md` | paste | The "panel of experts, be exhaustive, good/bad examples" prompt for any `*-standards.md` |
| `code-audit.md` | `/audit` command or Stop-time skill | Pre-commit self-review against the standards and the spec |
| `commit-skill/SKILL.md` | `.claude/skills/commit/` | How a commit is made in this repo (Cherny-style inner-loop automation) |
| `lesson-to-rule.md` | `/lesson` | Turns an agent mistake into a `CLAUDE.md` line, a rule, a test, or a hook (the ratchet) |

Commands: copy a file to `<repo>/.claude/commands/<name>.md` (Claude Code) — the frontmatter `description` is already there. For Cursor/Codex, keep them in `prompts/` and paste.

## Adapt

- Replace `<<…>>` with the repo's test/lint commands and doc paths.
- Keep prompts short at the top (what to do) and detailed below (how); agents read the first lines most reliably.

## Verify

- `/ask-expert` on a vague request returns ≥ 8 grouped questions and no code.
- `/audit` before a commit lists concrete standard violations with file:line, or explicitly "none found" per section.
- `/lesson` after a mistake proposes an enforcement mechanism, not just a sentence.

## Sources

- LIDR videos C and D (meta-prompt, ask-the-expert, README-by-index, OpenAPI prompt, standards via expert personas); Boris Cherny (slash commands for inner loops, commit workflow, `code-simplifier`/`verify-app` subagents, "add to CLAUDE.md every time Claude errs") — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2, §3.9.

## Change log

- 2026-09-08 — created.
