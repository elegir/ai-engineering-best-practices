#!/usr/bin/env bash
# kb-publish.sh — publish one improvement to the knowledge base the way the KB itself recommends:
#   check → branch → commit → push → merge into main → push main → delete the branch (remote + local).
# Usage: scripts/kb-publish.sh "<slug>" "<commit message>"
#   e.g. scripts/kb-publish.sh add-openai-harness-source "kb: add 2026-09-15 OpenAI harness-engineering source"
# Works with plain git; if the GitHub CLI (gh) is installed and authenticated it opens and merges a PR instead,
# so the change shows up in the PR history. Never uses --no-verify, never force-pushes.
set -euo pipefail
SLUG="${1:?slug required (kebab-case)}"
MSG="${2:?commit message required}"
BRANCH="kb/${SLUG}"
MAIN="main"

cd "$(git rev-parse --show-toplevel)"

# 0. Sanity: must start clean on main, up to date
CUR="$(git rev-parse --abbrev-ref HEAD)"
if [ "$CUR" != "$MAIN" ]; then echo "Switch to $MAIN first (currently on $CUR)."; exit 1; fi
git fetch origin "$MAIN" -q 2>/dev/null || true
if git rev-parse --verify -q "origin/$MAIN" >/dev/null; then git merge --ff-only "origin/$MAIN" -q; fi
if [ -z "$(git status --porcelain)" ]; then echo "Nothing to publish (working tree clean)."; exit 0; fi

# 1. The KB's own sensor
bash scripts/kb-check.sh

# 2. Branch + commit
git checkout -b "$BRANCH"
git add -A
git commit -m "$MSG"

# 3. Push branch
git push -u origin "$BRANCH"

# 4. Merge into main and clean up
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  gh pr create --base "$MAIN" --head "$BRANCH" --title "$MSG" --body "Published with scripts/kb-publish.sh. See INDEX.md for the entry." >/dev/null
  gh pr merge "$BRANCH" --squash --delete-branch --admin >/dev/null 2>&1 || gh pr merge "$BRANCH" --squash --delete-branch
  git checkout "$MAIN"
  git pull --ff-only origin "$MAIN"
else
  git checkout "$MAIN"
  git merge --no-ff "$BRANCH" -m "merge: $BRANCH"
  git push origin "$MAIN"
  git push origin --delete "$BRANCH"
fi
git branch -D "$BRANCH" 2>/dev/null || true
git remote prune origin >/dev/null 2>&1 || true

echo "Published: $MSG"
echo "main is at $(git rev-parse --short HEAD); branch $BRANCH deleted."
