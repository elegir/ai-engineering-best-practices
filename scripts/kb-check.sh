#!/usr/bin/env bash
# kb-check.sh — the knowledge base verifies itself before every publish (its own "sensor").
# Checks: frontmatter present with a status; INDEX.md lists every principle/practice/source/decision/playbook;
# no dangling relative links; no lingering <<PLACEHOLDER>> outside practices/ and templates/.
# Usage: scripts/kb-check.sh   (exit 0 = ok, 1 = problems listed)
set -u
cd "$(dirname "$(readlink -f "$0")")/.." || exit 1
fail=0
say() { echo "  - $*"; fail=1; }

echo "[1/4] frontmatter"
for f in principles/*.md decisions/*.md playbooks/*.md sources/*.md practices/*/README.md; do
  [ -f "$f" ] || continue
  head -n1 "$f" | grep -q '^---$' || say "$f: missing frontmatter"
  grep -Eq '^status: *(current|draft|superseded|accepted|proposed|deprecated)' "$f" || say "$f: missing/invalid status"
done

echo "[2/4] INDEX.md coverage"
for f in principles/*.md decisions/*.md playbooks/*.md sources/*.md; do
  grep -Fq "$f" INDEX.md || say "$f not listed in INDEX.md"
done
for d in practices/*/; do
  [ "$d" = "practices/_template/" ] && continue
  grep -Fq "$d" INDEX.md || say "$d not listed in INDEX.md"
done

echo "[3/4] relative links"
grep -rhoE '`(principles|sources|playbooks|templates|decisions|practices|skills)/[A-Za-z0-9_./-]+`' --include=*.md . \
  | tr -d '`' | sort -u | while read -r p; do
    case "$p" in *YYYY*|*NNNN*|*NN-*|*slug*|*…*) continue;; esac
    [ -e "$p" ] || echo "  - broken link: $p"
  done | tee /tmp/kb-links.txt
[ -s /tmp/kb-links.txt ] && fail=1

echo "[4/4] placeholders outside practices/ and templates/"
# The literal tokens <<PLACEHOLDER>> and <<LIKE_THIS>> are how the convention itself is documented; anything else is a real leftover.
grep -rhoE '<<[A-Za-z0-9 _./-]+>>' --include=*.md principles sources decisions playbooks AGENTS.md INDEX.md CONVENTIONS.md 2>/dev/null \
  | grep -vE '^<<(PLACEHOLDER|LIKE_THIS)>>$' | sort -u > /tmp/kb-placeholders.txt
if [ -s /tmp/kb-placeholders.txt ]; then sed 's/^/  - leftover placeholder outside practices\/templates: /' /tmp/kb-placeholders.txt; fail=1; fi

if [ $fail -eq 0 ]; then echo "kb-check: OK"; exit 0; else echo "kb-check: problems found"; exit 1; fi
