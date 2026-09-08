# Frontend standards

<!-- Delete this file if the repo has no UI. Same rule as backend: rule + why + good/bad example per section. -->

## 1. Overview
Framework, version, rendering model (SPA/SSR), state management, styling approach, component library. Link `stack.md`.

## 2. Project structure
Folders for pages/routes, components (shared vs feature), hooks/composables, API client, styles, assets, tests.

## 3. Components
- Composition rules; size limit; props typing; no business logic in components (where it goes instead).
- Naming; one component per file; co-located test and story if used.

## 4. State and data fetching
- Server state vs UI state; the single API client; error and loading states are mandatory.

## 5. Forms and validation
- Library; schema shared with backend if possible; error display rules; never trust client validation alone.

## 6. Accessibility
- Semantic HTML; keyboard navigation; ARIA only when needed; color contrast; automated check in e2e (<<axe>>).

## 7. Styling
- Approach (utility CSS / modules / design tokens); no inline styles except dynamic values; responsive breakpoints.

## 8. Performance
- Code splitting; image handling; bundle budget; avoid re-render traps.

## 9. Security
- Never render unsanitized HTML; token storage policy; CSP if any.

## 10. Testing (summary)
- Component tests for logic; e2e through the real UI for flows (Playwright); accessibility-tree selectors (role/name) over CSS selectors.

## 11. Definition of done for UI changes
Works on the supported browsers/viewports · e2e covers the flow · accessibility check passes · docs/screens updated if the flow changed.
