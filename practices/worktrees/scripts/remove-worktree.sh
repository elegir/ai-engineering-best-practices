#!/usr/bin/env bash
# Usage: scripts/remove-worktree.sh <ticket-slug>   (run from the main checkout after the branch is merged)
set -euo pipefail
SLUG="${1:?ticket slug required}"
REPO_DIR="$(git rev-parse --show-toplevel)"
WT_DIR="$(dirname "$REPO_DIR")/$(basename "$REPO_DIR")-${SLUG}"
SAFE="$(printf '%s' "$SLUG" | tr -c 'a-zA-Z0-9' '_' | tr 'A-Z' 'a-z')"
DB_NAME="<<appdb>>_${SAFE}"

git -C "$REPO_DIR" branch --merged | grep -q " $SLUG$" || { echo "Branch $SLUG is not merged; refusing. Merge first or pass --force manually."; exit 1; }
<<dropdb "$DB_NAME" 2>/dev/null || true>>
git -C "$REPO_DIR" worktree remove "$WT_DIR"
git -C "$REPO_DIR" worktree prune
git -C "$REPO_DIR" branch -d "$SLUG"
echo "Removed worktree $WT_DIR, branch $SLUG, db $DB_NAME"
