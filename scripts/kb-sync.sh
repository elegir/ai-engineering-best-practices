#!/usr/bin/env bash
# kb-sync.sh — is this copy of the knowledge base current? Run at the start of every session (in the KB itself
# or from another repo that consults it). Writes only inside .git/ (a fetch); with --pull it also fast-forwards
# main when this copy is only BEHIND and clean — safe, no merge, no rebase, nothing of yours is touched.
#   bash scripts/kb-sync.sh          → fetch, report ahead/behind, exit 1 if not in sync (working tree untouched)
#   bash scripts/kb-sync.sh --pull   → additionally fast-forward main when this copy is only BEHIND
# Never rebases, never force-pushes, never touches uncommitted work. If this copy is AHEAD (commits never pushed),
# it tells you the one command to run; publishing stays with kb-publish.sh.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
MAIN="main"
git fetch origin "$MAIN" -q
CUR="$(git rev-parse --abbrev-ref HEAD)"
AHEAD="$(git rev-list --count "origin/$MAIN..HEAD")"
BEHIND="$(git rev-list --count "HEAD..origin/$MAIN")"
DIRTY="$(git status --porcelain | wc -l | tr -d ' ')"
echo "kb-sync: branch=$CUR ahead=$AHEAD behind=$BEHIND uncommitted=$DIRTY (origin/$MAIN = $(git rev-parse --short "origin/$MAIN"))"
if [ "$AHEAD" -eq 0 ] && [ "$BEHIND" -eq 0 ]; then echo "kb-sync: in sync with origin/$MAIN."; exit 0; fi
if [ "$AHEAD" -gt 0 ]; then
  echo "kb-sync: this copy has $AHEAD commit(s) that were NEVER PUSHED:"; git log --oneline "origin/$MAIN..HEAD" | sed 's/^/    /'
  echo "kb-sync: publish them before doing anything else:  git push origin $CUR:kb/local-unpushed-$(date +%F)   (then merge via kb-publish flow)"
fi
if [ "$BEHIND" -gt 0 ]; then
  echo "kb-sync: this copy is $BEHIND commit(s) BEHIND origin/$MAIN:"; git log --oneline "HEAD..origin/$MAIN" | head -15 | sed 's/^/    /'
  if [ "${1:-}" = "--pull" ] && [ "$AHEAD" -eq 0 ] && [ "$DIRTY" -eq 0 ] && [ "$CUR" = "$MAIN" ]; then
    git merge --ff-only "origin/$MAIN" -q && echo "kb-sync: fast-forwarded to origin/$MAIN." && exit 0
  fi
  echo "kb-sync: update with:  bash scripts/kb-sync.sh --pull   (only when ahead=0 and nothing uncommitted, on $MAIN)"
fi
exit 1
