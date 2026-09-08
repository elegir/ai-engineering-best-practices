---
description: Publish one KB improvement — check, branch, commit, push, merge to main, delete branch. Usage: /publish <slug> <commit message>
---

Publish the current working-tree changes as one improvement.

1. Run `!bash scripts/kb-check.sh`. If it reports problems, fix them first (frontmatter, INDEX.md coverage, links, leftover placeholders) and re-run. Do not skip.
2. Parse `$ARGUMENTS`: the first word is the slug (kebab-case), the rest is the commit message. If either is missing, propose them from the diff (`!git status --short`) and ask.
3. Run `!bash scripts/kb-publish.sh "<slug>" "<message>"`.
4. Report: files changed, commit hash on `main`, confirmation that branch `kb/<slug>` was deleted, and anything the check flagged.
