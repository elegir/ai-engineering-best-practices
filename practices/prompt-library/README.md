---
title: "Practice — prompt library (the prompts that generate context and discipline)"
type: practice
status: current
date: 2026-09-08
last-reviewed: 2026-09-30
tags: [prompts, meta-prompt, ask-the-expert, commands, skills]
kind: working-style
applies-when: "always"
reference-status: untested   # untested | field-tested | reference (decision 0005 §3)
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
| `implement-practice.md` | `/implement-practice <name>` | Implement any KB practice in any stack: contract (Verify) → stack-sensitive points → reference by authority order → prove with negatives → field report (decision 0005 §9) |
| `meta-prompt.md` | `/meta` command or paste | Turns a one-line request into a structured ROLE/CONTEXT/OBJECTIVE/REQUIREMENTS/FORMAT/QUALITY prompt |
| `ask-the-expert.md` | `/ask-expert` | Forces clarification questions before any design or implementation |
| `readme-by-index.md` | paste | One-shot template: fill a fixed index, never invent structure |
| `openapi-from-code.md` | paste | Generate/refresh `docs/api-spec.yml` |
| `standards-document.md` | paste | The "panel of experts, be exhaustive, good/bad examples" prompt for any `*-standards.md` |
| `code-audit.md` | `/audit` command or Stop-time skill | Pre-commit self-review against the standards and the spec |
| `commit-skill/SKILL.md` | `.claude/skills/commit/` | How a commit is made in this repo (Cherny-style inner-loop automation) |
| `lesson-to-rule.md` | `/lesson` | Turns an agent mistake into a `CLAUDE.md` line, a rule, a test, or a hook (the ratchet) |

Commands: copy a file to `<repo>/.claude/commands/<name>.md` (Claude Code) — the frontmatter `description` is already there. For Cursor/Codex, keep them in `prompts/` and paste.

## Reference implementation

The prompt files themselves are the reference; `commit-skill/SKILL.md` shows the Agent-Skills packaging. They contain no stack-specific text except the audit prompt's example commands, which the repo replaces with its own from `docs/development-guide.md`.

## Stack-sensitive points

- Installation location is tool-dependent (Claude Code `.claude/commands/`, Cursor rules, a skills folder), not stack-dependent.
- The code-audit prompt needs the repo's standards documents to exist (`../context-docs-skeleton/`); on a WordPress repo those standards are mostly WordPress coding standards plus the repo's own additions — say which.

## Adapt

- Replace `<<…>>` with the repo's test/lint commands and doc paths.
- Keep prompts short at the top (what to do) and detailed below (how); agents read the first lines most reliably.

## Verify

Each numbered line is a stack-neutral assertion — the contract (decision 0005 §2). `observer` says who can judge it: `script` (a command's exit code), `agent` (the agent observes it in a session), `Martin` (a human reads it). `negative` is what must make it fail. `framework: beats` means the assertion wins over the repo's existing framework or library; `bends` means the repo's idiom wins and the assertion adapts to it. Stack-specific commands live only under *Example commands (Python)*.

1. The ask-the-expert prompt, given a vague request, returns at least eight grouped questions and writes no code — observer: agent — negative: code in the answer, or fewer than eight questions
2. The code-audit prompt, run before a commit, lists concrete standard violations with file and line, or states "none found" per section of the standards — observer: agent — negative: a vague "looks fine", or a violation without a location
3. The lesson-to-rule prompt, after a mistake, proposes a mechanical enforcement (hook, test, lint) and not only a sentence for the entry file — observer: Martin — negative: a lesson that becomes prose and nothing else
4. The implementation prompt (`implement-practice.md`), run on a practice, produces work judged only by that practice's `## Verify` and ends with a field report — observer: Martin — negative: an adoption with no field report, or one judged by "it looks done"
5. The prompts are installed where the agent finds them (commands folder, rules, or skill) and each is reachable by one short invocation — observer: agent — negative: a prompt that must be pasted by hand each time

**Example commands (Claude Code):** `/ask-expert`, `/audit`, `/lesson`, `/implement-practice llm-api-calls`.

## Sources

- LIDR videos C and D (meta-prompt, ask-the-expert, README-by-index, OpenAPI prompt, standards via expert personas); Boris Cherny (slash commands for inner loops, commit workflow, `code-simplifier`/`verify-app` subagents, "add to CLAUDE.md every time Claude errs") — `sources/2026-09-08-lidr-workshop-harness-engineering.md` §3.2, §3.9.

## Change log

- 2026-09-30 — decision 0005: Verify rewritten as the structured contract (observer / negative / framework); `## Reference implementation` and `## Stack-sensitive points` added; `reference-status: untested` until a real repo passes this Verify. Source `sources/2026-09-30-stack-debate.md`.
- 2026-09-26 — added `kind` and `applies-when` frontmatter (decision 0003).

- 2026-09-08 — created.

- 2026-09-24 — added `trajectory-review.md` ("think like your agent": model-assisted review of context and trajectories; principle 21).
