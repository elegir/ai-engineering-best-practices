# Stack-notes — Node / TypeScript

Fast, Rust-based tools so the PostToolUse loop finishes in milliseconds.

| Purpose | Tool | Command |
|---|---|---|
| Format | Biome | `npx biome format --write <file>` |
| Lint (fast) | Biome or Oxlint | `npx biome lint <file>` / `npx oxlint <file>` |
| Lint (custom rules, CI only) | ESLint + `eslint-plugin-local-rules` | `npx eslint .` |
| Types | tsc | `npx tsc --noEmit` |
| Unit | Vitest / Jest | `npx vitest run` / `npm test -- --silent` |
| E2E | Playwright | `npx playwright test` |
| Hooks | Lefthook | `npm i -D lefthook && npx lefthook install` |

Rules worth enforcing at error level: `noExplicitAny`, unused imports, no default exports (grep-ability), max file length ~400 lines, import boundaries between layers (Biome `noRestrictedImports` or ESLint boundaries plugin).

Install: `npm i -D @biomejs/biome lefthook` · `npx biome init`.

**Lines for `hooks.json`** (2026-09-30): `"format": {".ts": "npx biome format --write {file}", ".tsx": …, ".js": …}`, `"lint": {".ts": "npx biome lint {file}", …}`, `"stop_test_command": "npm test -- --silent"` (or `npx vitest run`). Pitfall: `npx` resolves the project's binary, so the first `npx biome` after a fresh clone is slow; run it once before trusting the sixty-second budget.
