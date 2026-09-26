#!/usr/bin/env bash
# kb-check.sh — the knowledge base verifies itself before every publish (its own "sensor").
# Checks: frontmatter present with a status; INDEX.md lists every principle/practice/source/decision/playbook;
# no dangling relative links; no lingering <<PLACEHOLDER>> outside practices/ and templates/.
# Usage: scripts/kb-check.sh   (exit 0 = ok, 1 = problems listed)
set -u
cd "$(dirname "$(readlink -f "$0")")/.." || exit 1
fail=0
say() { echo "  - $*"; fail=1; }

echo "[1/5] frontmatter"
for f in principles/*.md decisions/*.md playbooks/*.md sources/*.md practices/*/README.md; do
  [ -f "$f" ] || continue
  head -n1 "$f" | grep -q '^---$' || say "$f: missing frontmatter"
  grep -Eq '^status: *(current|draft|superseded|accepted|proposed|deprecated)' "$f" || say "$f: missing/invalid status"
done

echo "[2/5] INDEX.md coverage"
for f in principles/*.md decisions/*.md playbooks/*.md sources/*.md; do
  grep -Fq "$f" INDEX.md || say "$f not listed in INDEX.md"
done
for d in practices/*/; do
  [ "$d" = "practices/_template/" ] && continue
  grep -Fq "$d" INDEX.md || say "$d not listed in INDEX.md"
done

echo "[3/5] relative links"
grep -rhoE '`(principles|sources|playbooks|templates|decisions|practices|skills)/[A-Za-z0-9_./-]+`' --include=*.md . \
  | tr -d '`' | sort -u | while read -r p; do
    case "$p" in *YYYY*|*NNNN*|*NN-*|*slug*|*…*) continue;; esac
    [ -e "$p" ] || echo "  - broken link: $p"
  done | tee /tmp/kb-links.txt
[ -s /tmp/kb-links.txt ] && fail=1

echo "[4/5] applicability: kind + applies-when on every practice, vocabulary words only, row in practices/README.md"
vocab="$(grep -oE '^\| `[a-z_]+` \|' practices/facts.md | tr -d '`| ' | tr '\n' ' ')"
for d in practices/*/; do
  [ "$d" = "practices/_template/" ] && continue
  f="$d/README.md"; name="$(basename "$d")"
  grep -Eq '^kind: *(working-style|capability)$' "$f" || say "$f: missing/invalid kind"
  aw="$(grep -E '^applies-when:' "$f" | head -n1 | sed -E 's/^applies-when: *"?//; s/"? *$//')"
  [ -n "$aw" ] || { say "$f: missing applies-when"; continue; }
  for w in $(echo "$aw" | tr -c 'a-z_' ' '); do
    case " always and or not $vocab " in *" $w "*) ;; *) say "$f: applies-when uses undeclared word '$w' (add it to practices/facts.md)";; esac
  done
  grep -Fq "| \`$name/\` |" practices/README.md || say "$d: no row in practices/README.md table"
done

echo "[5/5] placeholders outside practices/ and templates/"
# The literal tokens <<PLACEHOLDER>> and <<LIKE_THIS>> are how the convention itself is documented; anything else is a real leftover.
grep -rhoE '<<[A-Za-z0-9 _./-]+>>' --include=*.md principles sources decisions playbooks AGENTS.md INDEX.md CONVENTIONS.md 2>/dev/null \
  | grep -vE '^<<(PLACEHOLDER|LIKE_THIS)>>$' | sort -u > /tmp/kb-placeholders.txt
if [ -s /tmp/kb-placeholders.txt ]; then sed 's/^/  - leftover placeholder outside practices\/templates: /' /tmp/kb-placeholders.txt; fail=1; fi

if [ $fail -eq 0 ]; then echo "kb-check: OK"; exit 0; else echo "kb-check: problems found"; exit 1; fi
