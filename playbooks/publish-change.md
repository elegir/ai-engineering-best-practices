---
title: "Playbook — publish a change to the knowledge base (branch → commit → push → merge → delete branch)"
type: playbook
status: current
date: 2026-09-08
last-reviewed: 2026-09-08
tags: [git, github, publish, self-maintenance]
sources:
  - principles/05-verification-loops.md
  - principles/09-knowledge-base-design.md
supersedes: null
superseded-by: null
---

# Publish a change to the knowledge base

The KB follows its own advice: every improvement is verified by a mechanical check, lands through a short-lived branch, and leaves `main` clean with the branch deleted. One script does it; this playbook says when and how.

## When

After any ingestion (`ingest-new-source.md`), any correction to a principle or practice, or any structural change. One improvement = one publish. Do not batch a week of unrelated edits into one commit.

## Steps (agent or human)

1. Make sure you are on `main` with the working tree containing only this improvement (`git status`).
2. Run the KB's own sensor: `bash scripts/kb-check.sh`. Fix anything it reports (missing frontmatter/status, file not in `INDEX.md`, broken relative link, stray `<<PLACEHOLDER>>` outside `practices/`/`templates/`).
3. Publish:
   ```bash
   bash scripts/kb-publish.sh <slug> "<commit message>"
   # example
   bash scripts/kb-publish.sh add-2026-09-15-openai-harness "kb: add 2026-09-15 OpenAI harness-engineering source; update principles 02, 03"
   ```
   The script: re-runs the check → creates `kb/<slug>` → commits → pushes → merges into `main` (via a squashed PR when `gh` is authenticated, otherwise a `--no-ff` merge) → pushes `main` → deletes the branch on GitHub and locally.
4. Report to Martin: what changed (files), the commit hash, and any items the check flagged.

Claude Code shortcut: `/publish <slug> <message>` (defined in `.claude/commands/publish.md`).

## Commit message convention

`kb: <verb> <what> [; <secondary effect>]` — e.g. `kb: add 2026-09-08 LIDR workshop source`, `kb: supersede model table in principle 08`, `kb: add practice worktrees/ (windows scripts)`. Always in English, imperative, under 72 characters for the first line.

## Rules

- Never `--no-verify`, never force-push, never commit directly on `main` (the script refuses if the tree is dirty on `main` only in the sense that it moves the work to a branch first — but do not `git commit` on `main` by hand).
- `INDEX.md` changes in the same publish as the files it lists.
- If the check fails, the publish stops. Fix, then re-run. Do not skip the check.
- Windows: run from Git Bash (or from the Cowork VM). `gh` is optional; without it the script uses plain git with the credentials already configured on the machine.
