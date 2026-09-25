# INDEX

Every file in this knowledge base, one line each. Update in the same commit as any addition or status change. Agents: if it is not listed here, assume it does not exist.

## Chronological log of sources

| Date | Source | Type | Raw material |
|---|---|---|---|
| 2026-09-08 | `sources/2026-09-08-lidr-workshop-harness-engineering.md` — LIDR workshop "De Developer a AI Champion: Harness Engineering" (Álvaro Moya) + 5 embedded videos | workshop | `sources/raw/2026-09-08-lidr-workshop/` (Notion full text; 5 YouTube transcripts) |
| 2026-09-08 | `sources/2026-09-08-how-teams-structure-agent-knowledge.md` — web survey: how pros structure knowledge for agents (OpenAI, practitioner guide, awesome-harness-engineering, SIGPLAN, docs stack, Agent Skills, Claude Code memory docs, LIDR article) | research | — |
| 2026-09-24 | `sources/2026-09-24-market-scan-s12-intro-to-agents.md` — market scan for LIDR session 12 "Introduction to AI agents": 105 YouTube results + 30 podcast shows considered, 15 items selected and transcribed (Anthropic, AI Engineer, Stanford, Google Cloud, Cursor, IBM, Latent Space). Log only; digest pending | market scan | `sources/raw/2026-09-24-market-scan-s12-agents/` (15 transcripts, 2 search-result JSON) |
| (living) | `sources/media-registry.json` + `sources/media-registry.md` — every video/podcast episode ever considered, with status (transcribed / digested / applied / candidate / discarded) and reason; filtered by `scripts/scan-filter.py` | registry | — |
| (living) | `sources/scan-log.md` — one row per course module: stage reached (mapped → catalogued → scanned → transcribed → digested → principled → validated) | tracking | — |

## Principles (current answers by topic)

| # | File | Status | Last reviewed |
|---|---|---|---|
| 00 | `principles/00-glossary.md` | current | 2026-09-08 |
| 01 | `principles/01-context-engineering.md` | current | 2026-09-08 |
| 02 | `principles/02-harness-engineering.md` | current | 2026-09-08 |
| 03 | `principles/03-agent-instruction-files.md` | current | 2026-09-08 |
| 04 | `principles/04-spec-driven-development.md` | current | 2026-09-08 |
| 05 | `principles/05-verification-loops.md` | current | 2026-09-08 |
| 06 | `principles/06-parallel-agents-and-worktrees.md` | current | 2026-09-08 |
| 07 | `principles/07-token-economy.md` | current | 2026-09-08 |
| 08 | `principles/08-model-selection.md` | current (model names dated 2026-09-08) | 2026-09-08 |
| 09 | `principles/09-knowledge-base-design.md` | current | 2026-09-08 |

## Practices (applicable — copyable files with "applies when", adapt and verify sections)

| Practice | Implements | Files | Status | Last reviewed |
|---|---|---|---|---|
| `practices/context-docs-skeleton/` | 01 | 9 `docs/` skeletons + `prompts/generate-docs.md` | current | 2026-09-08 |
| `practices/agent-entry-file/` | 03 | `AGENTS.md`, `CLAUDE.md`, `CLAUDE.local.md.example`, `.claude/rules/api.md`, Cursor pointer | current | 2026-09-08 |
| `practices/hooks-and-guards/` | 02, 05 | `.claude/settings.json`, 4 hook scripts, `lefthook.yml`, variants node/python/php-wordpress | current | 2026-09-08 |
| `practices/session-state/` | 02 | `PROGRESS.json`, `/start-session`, `/end-session`, startup routine | current | 2026-09-08 |
| `practices/worktrees/` | 06 | `.worktreeinclude`, `new-worktree.sh/.ps1`, `remove-worktree.sh`, `isolation.md` | current | 2026-09-08 |
| `practices/verification/` | 05 | Playwright smoke, Hurl smoke, pytest smoke, bats, definition-of-done, harness-evals | current | 2026-09-08 |
| `practices/spec-driven/` | 04 | `specs/README.md`, `/plan-ticket`, `/develop-task`, `constitution.md`, OpenSpec quickstart | current | 2026-09-08 |
| `practices/prompt-library/` | 01, 04 | meta-prompt, ask-the-expert, readme-by-index, openapi, standards-doc, `/audit`, commit skill, `/lesson` | current | 2026-09-08 |
| `practices/token-savings/` | 07 | ordered checklist, MCP audit, measurement log | current | 2026-09-08 |
| `practices/_template/` | — | README template for new practices | — | — |

## Decisions

| # | File | Status |
|---|---|---|
| 0001 | `decisions/0001-knowledge-base-structure.md` — single local KB consulted by pointer | accepted |
| 0002 | `decisions/0002-market-scan-protocol-and-media-registry.md` — fixed market-scan protocol; registry of every video/podcast considered; new scans only look at new items | accepted |

## Playbooks

| File | Purpose |
|---|---|
| `playbooks/adopt-kb-in-a-repo.md` | Make a repo point to this KB (Windows-safe, no symlinks) |
| `playbooks/audit-repo-against-kb.md` | Inventory → score → findings → plan → stop for approval |
| `playbooks/ingest-new-source.md` | Turn raw material into a source entry + principle/practice updates |
| `playbooks/publish-change.md` | Ship one improvement: check → branch → commit → push → merge → delete branch (`scripts/kb-check.sh`, `scripts/kb-publish.sh`, `/publish`) |
| `playbooks/scan-market-for-module.md` | For one course module: search YouTube + podcasts with Apify, select by authority, transcribe, log what was considered/selected/discarded, update `sources/scan-log.md` |

## Templates

`templates/source-entry.md` · `templates/principle.md` · `templates/decision.md` · `templates/open-spec-user-story.md` (with SSO sign-up/login worked examples)

## Scripts

`scripts/kb-check.sh` — self-verification (frontmatter, index coverage, links, placeholders) · `scripts/kb-publish.sh` — branch/commit/push/merge/cleanup · `scripts/scan-filter.py` — drop already-registered media from a new scan result

## Skills

`skills/apply-ai-engineering-kb/SKILL.md` — Agent-Skills-format entry point; copy to `~/.claude/skills/` to make it global.

## Topic map

| Topic | Principle (why) | Practice (how) | Sources |
|---|---|---|---|
| AI Champion / agentic engineer / harness engineer roles | `00-glossary.md` | — | workshop §3.1, video A |
| Context docs, standards, workflow, definition of done | `01-context-engineering.md` | `context-docs-skeleton/` | workshop §3.3, videos B/D; research §3.1, §3.4 |
| Five harness areas, primitives, hooks, ratchet | `02-harness-engineering.md` | `hooks-and-guards/`, `session-state/` | workshop §3.4, video B; research §3.1–3.3, §3.8 |
| CLAUDE.md / AGENTS.md design, rules, imports | `03-agent-instruction-files.md` | `agent-entry-file/` | research §3.2, §3.7; workshop §3.2 |
| OpenSpec / Spec-Kit / Superpowers / Spec-Boot; ask-the-expert; plan mode | `04-spec-driven-development.md` | `spec-driven/` | workshop §3.4, videos C/D |
| Tests, e2e, Playwright, Stop hooks, evals | `05-verification-loops.md` | `verification/`, `hooks-and-guards/` | workshop §3.6, video D; research §3.2 |
| Worktrees, parallel sessions, subagents | `06-parallel-agents-and-worktrees.md` | `worktrees/` | workshop §3.4 |
| rtk, codegraph, caveman, ponytail, Headroom, routing | `07-token-economy.md` | `token-savings/` | workshop §3.5 |
| Opus/Sonnet/Gemini/Codex by phase | `08-model-selection.md` | `context-docs-skeleton/docs/workflow.md` §3 | workshop §3.2, video C |
| MCP servers (Context7, Playwright, Sentry, Snyk, Jira/Notion, Figma) | `02-harness-engineering.md`, `01-context-engineering.md` | `token-savings/mcp-audit.md` | workshop §3.2, videos C/E |
| Prompt techniques (meta-prompt, ask-the-expert, one-shot index, audit, lesson→rule) | `04-spec-driven-development.md`, `01-context-engineering.md` | `prompt-library/` | workshop §3.2, videos C/D |
| How this KB is structured | `09-knowledge-base-design.md` | `practices/README.md` | research (all) |
| Agents: anatomy, patterns, tool use / function calling, MCP as tool transport, agentic RAG | (pending: 21-agent-design-and-tools.md) | (pending: agent-patterns/) | market scan s12 (15 transcripts) |

## Open actions (from sources)

- [ ] Workshop homework 1: update each repo's technical context docs → run `audit-repo-against-kb.md` per repo.
- [ ] Workshop homework 2: draft the SSO open spec (sign-up, login) in one repo → `templates/open-spec-user-story.md`.
- [ ] Try `rtk` for a week; record results as a source.
- [ ] Try OpenSpec on one small AI SDR change; record results.
- [ ] Read METR and Faros originals; annotate workshop entry §4.
- [ ] Read Anthropic *Building Effective Agents* / *Writing Effective Tools*; add sources.
- [ ] Not captured from the workshop: Vimeo intro clip, attached presentation `.mp4`, Faros PDF, ~26 images.
