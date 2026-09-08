# AGENTS.md — <<PROJECT NAME>>

<<One sentence: what this system does.>> This file is a map. Details live in `docs/` — read them; do not infer conventions from random files.

## Commands
- Install: `<<npm ci>>` · Start: `<<docker compose up>>` · Health: `<<curl localhost:3000/health>>`
- Unit: `<<npm test>>` · Integration: `<<npm run test:integration>>` · E2E: `<<npx playwright test>>`
- Lint/format: `<<npm run lint && npm run format>>` · Types: `<<npm run typecheck>>`
- Full guide: `docs/development-guide.md`

## Start of every session
1. Read `PROGRESS.json` and `git log --oneline -20`.
2. Run `<<health command>>`; if it fails, fix the environment before any task.
3. Pick the next task from `PROGRESS.json`; work on one task at a time.

## Where things are
- `docs/README.md` — map of all technical docs. Most used: `docs/backend-standards.md`, `docs/testing-standards.md`, `docs/workflow.md` (definition of done).
- Specs: `<<specs/>>` · Decisions: `<<docs/adr/>>` · Progress: `PROGRESS.json`
- Skills/commands: `.claude/commands/`, `.claude/skills/`

## Non-negotiables (each is enforced)
- Never edit `.env*` or linter/formatter configs — PreToolUse hook blocks it.
- Never `git commit --no-verify`; never disable a lint rule inline without an ADR reference — pre-commit + review.
- Tests first (TDD); the Stop hook runs the suite; do not declare done while red.
- Update the matching `docs/*` file in the same change — `docs/documentation-standards.md` §2.
- One task per prompt; plan before implementing anything larger than one file — `docs/workflow.md`.
- Ask when the spec is ambiguous; write the question in `PROGRESS.json`; do not guess.

## Shared engineering knowledge base
Martin's AI-engineering best practices live in `../ai-engineering-best-practices/` (sibling folder, not part of this repo).
- Read `../ai-engineering-best-practices/AGENTS.md` before proposing changes to agent instructions, tooling, MCPs, testing strategy, specs, worktrees or workflow.
- To evaluate this repo against those practices, run `../ai-engineering-best-practices/playbooks/audit-repo-against-kb.md` and present a plan before changing anything.
- Copy practices from `../ai-engineering-best-practices/practices/`, adapted; never copy principles or sources into this repo.
