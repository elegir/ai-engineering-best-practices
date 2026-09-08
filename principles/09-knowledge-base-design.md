---
title: "Knowledge-base design — how to keep accumulated know-how usable by agents"
type: principle
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [knowledge-base, documentation, adr, progressive-disclosure, rot]
sources:
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
supersedes: null
superseded-by: null
---

# Knowledge-base design

## 1. The question this answers

How should a growing body of best practices, workshop notes and decisions be stored so that agents in *other* repositories can consult it reliably, tell current from stale, and apply it without copying it?

## 2. Short answer

Markdown in a git repo, separated by **how it ages**: immutable dated `sources/`, living `principles/` with status and review dates, append-only `decisions/`, executable `playbooks/` and a skill. A short pointer-style `AGENTS.md` at the root, an `INDEX.md` that is updated in every commit, one file per fact, links instead of copies. Other repos consult it by pointer (a line in their `CLAUDE.md`) and by running the audit playbook — never by copying files in. Review principles on a schedule; supersede, never delete.

## 3. Long explanation

### Separate by aging behavior

Agents cannot tell stale text from current truth; humans can, from social cues agents lack. So the structure must carry the cue:

- **Sources** are snapshots. A workshop said X on a date. They never become wrong; they become old. Immutable, dated in the filename.
- **Principles** are the current answer. They *will* change, so they carry `status` and `last-reviewed`, cite the sources they rest on, and keep a change log. When they change, the old text is either annotated or the file is marked `superseded` with a pointer — the ADR trick, applied to prose.
- **Decisions** are commitments with a status lifecycle (proposed → accepted → deprecated/superseded). An agent can act on `accepted` and ignore the rest.
- **Practices** are the applicable layer: for each principle, a folder of ready-to-copy files (configs, scripts, prompts, skeletons) with an "applies when / does not apply when" test, stack variants, adaptation notes and verification steps. Principles say why; practices are what an agent in another repo actually adopts. A principle with no practice is advice; keeping the two in sync is part of ingesting every source.
- **Playbooks** are procedures — the one place where step-by-step imperative text belongs, because it is meant to be executed.
- **Templates** keep new entries consistent, which keeps them parseable.

### Short entry, deep body, index

Progressive disclosure at repo scale: `AGENTS.md` says what the folder is and where to look; `INDEX.md` lists everything with one line each; the files carry the depth. A reader (human or agent) loads only what the task needs.

### Single source of truth

Each fact in one file; everything else links. The moment a principle restates a source's numbers, the numbers can drift; it should *cite* them instead. Other repos must not copy principles into their own docs — they point here — or the copies rot on their own timeline.

### Long-form, explicit, English

Martin's requirement, and it matches the SIGPLAN observation that agents "cannot rely on institutional memory, hallway conversations, or code review discussions": the reasoning has to be written out. Digests explain terms at first use, keep numbers with their sources, and separate fact / evidence / opinion.

### Gardening

OpenAI runs a "doc-gardening" agent; the practitioner guide runs garbage-collection agents. For this KB: a periodic (monthly) agent pass that lists principles with `last-reviewed` older than 90 days, checks their sources still exist, finds contradictions between principles, and proposes updates as a diff for Martin to accept. Never auto-delete.

### Consumption from other repos (Windows-safe)

- A prose pointer in each repo's `CLAUDE.md`/`AGENTS.md` — no context cost until the agent follows it.
- Optionally an `@../ai-engineering-best-practices/AGENTS.md` import (costs context at every launch; triggers a one-time external-import approval; skipped in Cowork desktop sessions) — not the default.
- The skill in `skills/apply-ai-engineering-kb/` copied to `~/.claude/skills/` makes "apply the KB" available everywhere by progressive disclosure.
- Symlinks are avoided because Windows requires admin/Developer Mode for them.

## 4. How to apply it (to this KB and any other)

1. Every new file: frontmatter per `CONVENTIONS.md`; one line in `INDEX.md`; a commit.
2. Every new source: update the affected principles' `last-reviewed` and change log, even if nothing changed ("reviewed against source X; no change").
3. Every quarter: run the gardening pass.
4. Never delete; supersede.

## 5. Anti-patterns

- One `BEST_PRACTICES.md` that grows forever with no dates.
- Copying the KB into each repo.
- Editing a source entry to "fix" what the speaker said.
- Principles without sources ("everyone knows…").
- Deleting old advice — the history of *why* it changed is part of the value.

## 6. Evidence & sources

- `sources/2026-09-08-how-teams-structure-agent-knowledge.md` (all sections).
- `decisions/0001-knowledge-base-structure.md`.

## 7. Change log

- 2026-09-08 — created.
- 2026-09-08 — added the `practices/` layer (applicable files per principle) after Martin clarified the KB must carry copyable, stack-adaptable examples, not only explanations.
