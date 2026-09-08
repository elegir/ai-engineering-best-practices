#!/usr/bin/env bash
# Usage: scripts/new-worktree.sh <ticket-slug> [base-branch]
# Creates ../<repo>-<slug> on branch <slug>, copies .worktreeinclude files, installs deps,
# assigns a port and database name, runs migrations and seed.
set -euo pipefail
SLUG="${1:?ticket slug required, e.g. T-003-sso-signup}"
BASE="${2:-main}"
REPO_DIR="$(git rev-parse --show-toplevel)"
REPO_NAME="$(basename "$REPO_DIR")"
WT_DIR="$(dirname "$REPO_DIR")/${REPO_NAME}-${SLUG}"
BRANCH="$SLUG"

git -C "$REPO_DIR" fetch -q origin "$BASE" || true
git -C "$REPO_DIR" worktree add -b "$BRANCH" "$WT_DIR" "origin/$BASE" 2>/dev/null \
  || git -C "$REPO_DIR" worktree add -b "$BRANCH" "$WT_DIR" "$BASE"

# Copy includes
if [ -f "$REPO_DIR/.worktreeinclude" ]; then
  grep -Ev '^\s*(#|$)' "$REPO_DIR/.worktreeinclude" | while read -r f; do
    [ -e "$REPO_DIR/$f" ] && mkdir -p "$WT_DIR/$(dirname "$f")" && cp -r "$REPO_DIR/$f" "$WT_DIR/$f"
  done
fi

# Deterministic port + DB name from the slug
SAFE="$(printf '%s' "$SLUG" | tr -c 'a-zA-Z0-9' '_' | tr 'A-Z' 'a-z')"
HASH=$(( $(printf '%s' "$SLUG" | cksum | cut -d' ' -f1) % 900 ))
PORT=$(( <<3100>> + HASH ))
DB_NAME="<<appdb>>_${SAFE}"

# Append/override in the worktree's .env (never touch the main checkout)
{
  echo ""; echo "# --- worktree overrides ($SLUG) ---"
  echo "APP_PORT=$PORT"
  echo "DATABASE_URL=<<postgres://app:app@localhost:5432/>>$DB_NAME"
} >> "$WT_DIR/.env"

cd "$WT_DIR"
<<npm ci>>                                  # install deps
<<createdb "$DB_NAME" 2>/dev/null || true>>  # create DB (see isolation.md for MySQL/SQLite/Docker)
<<npm run migrate>>
<<npm run seed>>

echo "Worktree ready: $WT_DIR  (branch $BRANCH, port $PORT, db $DB_NAME)"
echo "Start Claude Code here with: cd \"$WT_DIR\" && claude"
