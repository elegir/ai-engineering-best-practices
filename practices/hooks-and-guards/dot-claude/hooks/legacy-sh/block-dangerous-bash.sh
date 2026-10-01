#!/usr/bin/env bash
# PreToolUse guard for Bash. Blocks destructive or bypassing commands.
INPUT="$(cat)"
CMD="$(printf '%s' "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\(.*\)".*/\1/p' | head -n1)"
[ -z "$CMD" ] && exit 0

DENY=(
  'rm -rf'
  'git push --force' 'git push -f'
  'git commit[^|]*--no-verify'
  'git reset --hard'
  'DROP (TABLE|DATABASE|SCHEMA)'
  'TRUNCATE'
  'terraform (apply|destroy)'
  'kubectl (delete|apply)[^|]*prod'
  '<<wp db reset>>'
  '<<deploy.*production>>'
)

for p in "${DENY[@]}"; do
  if printf '%s' "$CMD" | grep -Eiq "$p"; then
    echo "BLOCKED: command matches a forbidden pattern ($p). If this is really needed, stop and ask Martin to run it." >&2
    exit 2
  fi
done
exit 0
