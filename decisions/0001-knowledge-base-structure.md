---
title: "0001 — Keep a single local AI-engineering knowledge base, consulted by pointer from every repo"
type: decision
status: accepted
date: 2026-09-08
tags: [knowledge-base, structure]
sources:
  - sources/2026-09-08-how-teams-structure-agent-knowledge.md
  - sources/2026-09-08-lidr-workshop-harness-engineering.md
supersedes: null
superseded-by: null
---

# 0001 — Knowledge-base structure

## Context

Martin attended his first harness-engineering workshop on 2026-09-08 and wants a place where best practices, recommendations and workshop material accumulate over time, written long-form in English, dated, and consultable by agents working in his other repositories under `Local Coding/` (AI SDR, Content Central, WordPress Fleet Control, Report Agent, Pagoralia, and others). Options considered: a Notion space; a wiki; a `BEST_PRACTICES.md` copied into each repo; a single separate git repository of Markdown.

## Decision

- Create `C:\Users\marti\Local Coding\ai-engineering-best-practices\` as a standalone git repository of Markdown.
- Structure: `AGENTS.md` (short pointer entry; `CLAUDE.md` imports it), `INDEX.md`, `CONVENTIONS.md`, `README.md`, and folders `sources/` (immutable dated digests + `raw/` verbatim material), `principles/` (living, with status and review dates — the *why*), `practices/` (one folder per applicable practice with copyable, stack-adaptable files, "applies when" tests and verification — the *how*), `decisions/` (this format), `playbooks/`, `templates/`, `skills/`.
- Every source ingested must update both the principle (what/why) and the practice (applicable files) it touches; a principle without a practice is considered incomplete.
- Language: English for all artifacts.
- Other repos consult it by a **prose pointer** in their `CLAUDE.md`/`AGENTS.md` and by running `playbooks/audit-repo-against-kb.md`. They do **not** copy files from it.
- New knowledge enters via `playbooks/ingest-new-source.md`: raw material → dated source entry → principle updates → index line → commit.
- Nothing is deleted; superseded content is marked and linked.

## Consequences

- Positive: one source of truth; works with every agent that reads Markdown; diffs and history for free; no symlinks (Windows-friendly); the agent can tell current from stale by frontmatter.
- Negative: someone (Martin or an agent) must keep `INDEX.md` and `last-reviewed` honest; long-form entries cost time to write; a pointer that is never followed is inert — the audit playbook must actually be run per repo.
- Follow-ups: adopt in each repo (`playbooks/adopt-kb-in-a-repo.md`); schedule a quarterly gardening pass; `git init` and first commit.

## Notes
- 2026-09-26 — reaffirmed by `decisions/0003-applicability-by-facts.md`: the applicability selector writes nothing into target repos.
