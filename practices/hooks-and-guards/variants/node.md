# Variant — Node / TypeScript

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
