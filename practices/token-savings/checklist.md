# Token-savings checklist (do in order; measure after each)

## 0. Baseline (5 min)
Note this week's usage from the provider's usage page and, in Claude Code, run `/context` at the start of a fresh session: write down the sizes of memory files, tools, and skills. Put it in `measurement-log.md`.

## 1. Free: context first (the biggest lever)
- `context-docs-skeleton/` in place → the agent reads `docs/testing-standards.md` instead of ten test files.
- `agent-entry-file/`: root file ≤ ~50 lines; long content moved to `docs/`, `.claude/rules/` (path-scoped), or skills (on demand).
- `session-state/`: `/start-session` reads `PROGRESS.json` instead of re-exploring.

## 2. Free: tool and MCP audit
Fill `mcp-audit.md`. Remove every server/tool unused in two weeks. Vercel cut 80% of tools and *improved* accuracy. In Claude Code, keep tool search enabled so schemas load on demand.

## 3. rtk — compress terminal output (claimed 60–90% on common commands)
```bash
# see https://github.com/rtk-ai/rtk for the current install (cargo/npm/binary); then:
rtk init            # hooks Claude Code so commands run through rtk
```
Expect: `git status`, test runs, `ls`, build logs arrive summarized. Measure a week.

## 4. Structured verification over screenshots
Playwright with accessibility-tree selectors and text assertions; screenshots only on failure (already in `verification/`). If using a browser MCP, prefer CLI/snapshot modes over full-tree dumps.

## 5. Model routing
`docs/workflow.md` §3: top tier plans, mid tier executes. In Cursor/Copilot, "Auto" for routine work. Measure cost per task, not just tokens.

## 6. codegraph — query a local code graph instead of walking files (claimed ~57%)
```bash
# see https://github.com/colbymchenry/codegraph for install; index the repo; expose to the agent as instructed
```
Best on large repos; skip for small ones.

## 7. Headroom — compress logs/test output before they count as input (claimed up to 95%)
https://github.com/headroomlabs-ai/headroom — useful when test suites are chatty; overlaps with rtk, so measure.

## 8. caveman (terser answers, claimed ~65% output) and ponytail (less over-built code, claimed 80–94% in over-construction)
https://github.com/JuliusBrussee/caveman · https://github.com/DietrichGebert/ponytail — last, and only if output verbosity is a real cost.

## 9. Compaction hygiene
Keep state in `PROGRESS.json` and git, not in the conversation, so `/compact` loses nothing; use a PreCompact hook to re-inject the current task if needed.

## Never
Disable tests, e2e, or hooks to save tokens. Delete prohibitions from the entry file that prevent expensive mistakes.
