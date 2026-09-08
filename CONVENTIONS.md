# Conventions for writing in this knowledge base

These rules exist so that an agent reading this folder in a year can tell what is current, what is old, and where every claim came from. Follow them for every file.

## 1. Filenames

- `sources/`: `YYYY-MM-DD-short-slug.md`. The date is the date of the event or publication, not the date you wrote the digest. Slug in lowercase, hyphen-separated, max ~6 words. Example: `2026-09-08-lidr-workshop-harness-engineering.md`.
- `principles/`: `NN-topic.md` with a two-digit prefix that fixes reading order. Example: `02-harness-engineering.md`.
- `decisions/`: `NNNN-slug.md`, four-digit sequential number. Example: `0001-knowledge-base-structure.md`.
- `playbooks/`: `verb-object.md`. Example: `audit-repo-against-kb.md`.
- `practices/`: one folder per practice, `kebab-case-noun/`, containing a `README.md` (frontmatter `type: practice`, plus `principle:` pointing at the principle it implements) and the copyable files. Placeholders inside copyable files are written `<<LIKE_THIS>>`. Stack variants go in `variants/` or per-stack subfolders. Template: `practices/_template/`.

## 2. Frontmatter (mandatory)

Every markdown file except `README.md`, `AGENTS.md`, `CLAUDE.md`, `INDEX.md` and this file starts with YAML frontmatter.

```yaml
---
title: Human-readable title
type: source | principle | practice | decision | playbook | template
status: current | draft | superseded | accepted | proposed | deprecated
date: 2026-09-08            # sources & decisions: the event/decision date
last-reviewed: 2026-09-08   # principles & playbooks: last time a human or agent confirmed it is still right
tags: [harness-engineering, context-engineering]
sources:                    # principles/decisions/playbooks: what they were built from
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
  - https://example.com/article
supersedes: null            # path of the file this replaces, if any
superseded-by: null         # path of the file that replaced this, if any
---
```

Status vocabulary:

- **Sources**: always `current` (they are snapshots; they do not go stale, they just get older).
- **Principles / playbooks**: `draft` (not yet trusted), `current` (trusted), `superseded` (kept for history; read `superseded-by`).
- **Decisions**: `proposed`, `accepted`, `deprecated` (with `superseded-by`).

## 3. Structure of a source entry

Long and digested. The point is that someone (or an agent) who was not there can understand not just *what* was said but *why it matters* and *what to do about it*. Use these sections in this order:

1. **Context** — what the event/article was, who gave it, when, what audience, where the original material lives (URLs).
2. **One-paragraph summary** — the whole thing in five sentences.
3. **Detailed digest** — section by section, in prose. Explain every term the first time it appears. Include the numbers, the names of tools, the exact commands shown.
4. **Claims worth checking** — anything stated as fact that you did not verify, with a note on how confident you are.
5. **What is contested / trade-offs** — where reasonable people disagree, or where the speaker's interest may bias the advice (e.g. a vendor recommending its own product).
6. **Implications for Martin's repos** — concrete, repo-by-repo if possible.
7. **Actions taken / to take** — checklist; link to the decision or principle files that were created or changed because of this source.
8. **Raw notes / transcript excerpts** — optional appendix; verbatim material that supports the digest.

## 4. Structure of a principle

A principle is the *current answer* to one question. Sections:

1. **The question this answers** (one sentence).
2. **Short answer** (one paragraph; what to do).
3. **Long explanation** (why; how it works; how to recognise when it is being done badly).
4. **How to apply it in a repo** (checklist; concrete files/commands).
5. **Anti-patterns** (what people do wrong).
6. **Evidence & sources** (links to `sources/` and URLs).
7. **Change log** (dated lines: what changed in this principle and which source triggered it).

## 4b. Structure of a practice README

Solves (symptoms in a repo) → Applies when → Does not apply when → Files in this folder (table: file, copy to, purpose) → Adapt (placeholders, variants, what to delete) → Verify (what the agent must observe) → Sources → Change log. Copyable files carry a short header comment saying what to replace.

## 5. Style

- English. Full sentences. Explain jargon at first use. Prefer "run `npm test` before every commit" over "test properly".
- Absolute dates (`2026-09-08`), absolute versions (`Sonnet 4.6`), never "now", "latest", "recent".
- Separate **fact** ("the speaker said X"), **evidence** ("study Y measured Z") and **opinion** ("I think"). Do not blend them.
- Numbers keep their source ("+242.7% incidents per PR, Faros AI 'Acceleration Whiplash' report as cited by LIDR, 2026-09-08").
- Link relative paths inside the repo; full URLs outside.
- Do not paste large copyrighted texts verbatim. Digest them. Short quotes with attribution are fine.

## 6. Updating, never silently overwriting

When new knowledge contradicts old knowledge:

- Keep the old text if it is still partially useful; add a dated **Change log** line.
- If the old text is wrong now, set `status: superseded`, add `superseded-by`, and create the replacement.
- Never delete a file. History is part of the value.

## 7. Index discipline

Every added or superseded file gets a line in `INDEX.md` in the same commit. An agent that cannot find something in `INDEX.md` should assume it does not exist.
