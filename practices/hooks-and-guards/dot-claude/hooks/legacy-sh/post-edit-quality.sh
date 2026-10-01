#!/usr/bin/env bash
# PostToolUse quality loop for Write|Edit|MultiEdit.
# 1) auto-format the edited file, 2) lint it, 3) return remaining violations to the agent
#    as hookSpecificOutput.additionalContext (plain stdout is NOT treated as context).
# Replace the <<…>> commands with the stack's tools (see ../../variants/).

INPUT="$(cat)"
FILE="$(printf '%s' "$INPUT" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)"
[ -z "$FILE" ] || [ ! -f "$FILE" ] && exit 0

FORMAT_CMD=""
LINT_CMD=""
case "$FILE" in
  *.ts|*.tsx|*.js|*.jsx|*.json)
    FORMAT_CMD="<<npx biome format --write \"$FILE\">>"
    LINT_CMD="<<npx biome lint \"$FILE\">>" ;;
  *.py)
    FORMAT_CMD="<<ruff format \"$FILE\">>"
    LINT_CMD="<<ruff check \"$FILE\">>" ;;
  *.php)
    FORMAT_CMD="<<vendor/bin/phpcbf \"$FILE\">>"
    LINT_CMD="<<vendor/bin/phpcs \"$FILE\">>" ;;
  *) exit 0 ;;
esac

# Auto-fix first (resolves ~40-50% of issues silently)
eval "$FORMAT_CMD" >/dev/null 2>&1 || true

# Lint; capture remaining problems
LINT_OUT="$(eval "$LINT_CMD" 2>&1)"
STATUS=$?
[ $STATUS -eq 0 ] && exit 0

# Escape for JSON
ESCAPED="$(printf '%s' "$LINT_OUT" | head -c 4000 | sed 's/\\/\\\\/g; s/"/\\"/g' | awk '{printf "%s\\n", $0}')"
cat <<EOF
{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"Lint violations remain in $FILE after auto-format. Fix them now (do not disable rules):\n$ESCAPED"}}
EOF
exit 0
