#!/usr/bin/env bash
# PreToolUse guard for Write|Edit|MultiEdit.
# Blocks the agent from editing files that must only change through a human decision.
# Exit code 2 = block, and stderr is shown to the agent as the reason.

INPUT="$(cat)"
FILE="$(printf '%s' "$INPUT" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)"
[ -z "$FILE" ] && exit 0

# Add repo-specific paths here (merged migrations, generated files, deploy manifests).
PROTECTED_PATTERNS=(
  '\.env'                      # .env, .env.local, .env.production …
  'package-lock\.json' 'pnpm-lock\.yaml' 'yarn\.lock' 'poetry\.lock' 'composer\.lock'
  '\.eslintrc' 'eslint\.config' 'biome\.json' '\.prettierrc' 'tsconfig\.json'
  'pyproject\.toml' 'ruff\.toml' 'setup\.cfg' 'mypy\.ini'
  'phpcs\.xml' '\.php-cs-fixer'
  'lefthook\.yml' '\.pre-commit-config\.yaml'
  '\.github/workflows/' '\.gitlab-ci\.yml'
  '\.claude/settings\.json' '\.claude/hooks/'
  '<<migrations/.*merged.*>>'
)

for p in "${PROTECTED_PATTERNS[@]}"; do
  if printf '%s' "$FILE" | grep -Eq "$p"; then
    echo "BLOCKED: '$FILE' is protected (pattern: $p). Ask Martin to change it manually; explain why the change is needed." >&2
    exit 2
  fi
done
exit 0
