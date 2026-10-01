# INDEX

Every file in this knowledge base, one line each. Update in the same commit as any addition or status change. Agents: if it is not listed here, assume it does not exist.

## Chronological log of sources

| Date | Source | Type | Raw material |
|---|---|---|---|
| 2026-09-08 | `sources/2026-09-08-lidr-workshop-harness-engineering.md` — LIDR workshop "De Developer a AI Champion: Harness Engineering" (Álvaro Moya) + 5 embedded videos | workshop | `sources/raw/2026-09-08-lidr-workshop/` (Notion full text; 5 YouTube transcripts) |
| 2026-09-08 | `sources/2026-09-08-how-teams-structure-agent-knowledge.md` — web survey: how pros structure knowledge for agents (OpenAI, practitioner guide, awesome-harness-engineering, SIGPLAN, docs stack, Agent Skills, Claude Code memory docs, LIDR article) | research | — |
| 2026-09-24 | `sources/2026-09-24-market-scan-s12-intro-to-agents.md` — market scan for LIDR session 12 "Introduction to AI agents": 105 YouTube results + 30 podcast shows considered, 15 items selected and transcribed (Anthropic, AI Engineer, Stanford, Google Cloud, Cursor, IBM, Latent Space). Log only; digest pending | market scan | `sources/raw/2026-09-24-market-scan-s12-agents/` (15 transcripts, 2 search-result JSON) |
| 2026-09-24 | `sources/2026-09-24-s12-agents-digest.md` — digest of the 15 session-12 transcripts with the impact table (21 findings → 1 new principle, 1 new practice, 5 principles reviewed/refined, 3 parked) | digest | (raw as above) |
| 2026-09-26 | `sources/2026-09-26-selector-research.md` — web research: how AWS lenses, Google SRE, OWASP ASVS/SAMM, NIST profiles, Thoughtworks, IDP scorecards, Azure workload guides and coding-agent rules make catalogues conditional | research | — |
| 2026-09-26 | `sources/2026-09-26-selector-debate.md` — proposal v1 for a project-profile selector, 18-point devil's-advocate attack, responses, agreed design v2 | debate | — |
| 2026-09-27 | `sources/2026-09-27-market-scan-s01-llm-setup.md` — market scan for LIDR session 1 "LLMs and environment setup": 105 YouTube results + 25 podcast episodes considered, 13 items selected and transcribed (OpenAI, Anthropic ×3, Cursor, JetBrains, DeepLearning.AI/Ng, Karpathy ×2, Pocock, Witteveen, IBM, Chain of Thought) | market scan | `sources/raw/2026-09-27-market-scan-s01-llm-setup/` |
| 2026-09-27 | `sources/2026-09-27-s01-llm-setup-digest.md` — digest of the 13 session-1 transcripts with the impact table (34 findings → 1 new principle, 1 new practice, 6 glossary entries, 8 principles reviewed/refined, 3 parked) | digest | `sources/raw/2026-09-27-market-scan-s01-llm-setup/` |
| 2026-09-27 | `sources/2026-09-27-market-scan-s02-context-caching.md` — market scan for LIDR session 2 "CAG: context, parameters, costs": 105 YouTube results + 9 podcast episodes considered, 16 items selected and transcribed (Claude, Google Cloud, AWS, LangChain ×2, AI Engineer ×2, Sequoia/Harrison Chase, Dex Horthy, Ebbelaar, Hugging Face, IBM ×3, Latent Space, Chain of Thought) | market scan | `sources/raw/2026-09-27-market-scan-s02-context-caching/` |
| 2026-09-27 | `sources/2026-09-27-s02-context-caching-digest.md` — digest of the 16 session-2 transcripts with the impact table (36 findings → 1 new principle, 1 new practice, 1 new fact word, 6 glossary entries, 8 principles reviewed/refined, 2 parked) | digest | `sources/raw/2026-09-27-market-scan-s02-context-caching/` |
| 2026-09-30 | `sources/2026-09-30-market-scan-s03-wrappers.md` — market scan for LIDR session 3 "Model wrappers and layered architecture": 118 YouTube results + 9 podcast episodes considered, 12 new items transcribed (AI Engineer ×2, EuroPython, API World, AI Engineering Podcast, Latent Space via Whisper, Mastra, Langfuse, PyCon DE, CNCF, Scala Days, Percona) + 5 reused | market scan | `sources/raw/2026-09-30-market-scan-s03-wrappers/` |
| 2026-09-30 | `sources/2026-09-30-s03-wrappers-digest.md` — digest with the impact table (32 findings → 1 new principle, 1 new practice, 6 glossary entries, 5 principles refined, 2 parked) | digest | — |
| 2026-09-30 | `sources/2026-09-30-stack-debate.md` — devil's advocate vs "contract + prompt + one Python reference, no per-stack ports": 15 attacks, two rounds; survived with conditions (structured Verify, stack-sensitive points, stack-notes, fail-closed guard, variant governance, two-arm experiment) → decision 0005 | debate | — |
| 2026-09-30 | `sources/2026-09-30-day-one-debate.md` — clean-context devil's advocate vs the day-one goal: 20 attacks, two rounds, six agreed changes before module 4 (decision 0004 pending; decision 0004 published 2026-09-30) | debate | — |
| (living) | `sources/catalog-written-canon.md` — the written canon per course session (docs, papers, articles, courses), registered with `type: written` so none is read twice; sessions 1–3 + cross-cutting as of 2026-09-30 | catalogue | — |
| (living) | `sources/media-registry.json` + `sources/media-registry.md` — every video/podcast episode ever considered, with status (transcribed / digested / applied / candidate / discarded) and reason; filtered by `scripts/scan-filter.py` | registry | — |
| (living) | `sources/scan-log.md` — one row per course module: stage reached (mapped → catalogued → scanned → transcribed → digested → principled → validated) | tracking | — |

## Principles (current answers by topic)

| # | File | Status | Last reviewed |
|---|---|---|---|
| 00 | `principles/00-glossary.md` | current | 2026-09-30 |
| 01 | `principles/01-context-engineering.md` | current | 2026-09-27 |
| 02 | `principles/02-harness-engineering.md` | current | 2026-09-27 |
| 03 | `principles/03-agent-instruction-files.md` | current | 2026-09-08 |
| 04 | `principles/04-spec-driven-development.md` | current | 2026-09-27 |
| 05 | `principles/05-verification-loops.md` | current | 2026-09-30 |
| 06 | `principles/06-parallel-agents-and-worktrees.md` | current | 2026-09-27 |
| 07 | `principles/07-token-economy.md` | current | 2026-09-27 |
| 08 | `principles/08-model-selection.md` | current (model names dated 2026-09-08) | 2026-09-30 |
| 09 | `principles/09-knowledge-base-design.md` | current | 2026-09-08 |
| 10 | `principles/10-llm-api-fundamentals.md` — what a model call is, what the model cannot do, prompt structure and iteration, tokens/caching, provider checklist (course session 1) | draft | 2026-09-30 |
| 11 | `principles/11-runtime-context-management.md` — the window as a budget; offload / reduce / retrieve / isolate / cache; compaction rules; prompt caching and KV-cache economics; long context vs CAG vs retrieval (course session 2) | draft | 2026-09-30 |
| 12 | `principles/12-llm-gateway-layer.md` — the layer between code and providers: fallback over retry, one retry owner, cooldown, timeouts per route, tiers and shedding, keys, model registry, streaming pipeline, OTel tracing, semantic-cache boundary (course session 3) | draft | 2026-09-30 |
| 21 | `principles/21-agent-design-and-tools.md` — workflow vs agent, minimal loop, tool design, CLI/MCP/skill, agentic RAG (numbered by course session; 10–20 reserved) | draft | 2026-09-30 |

## Practices (applicable — copyable files with "applies when", adapt and verify sections)

(Which practices apply to a repo: `practices/README.md` column "Applies when" + `practices/facts.md` + `playbooks/which-practices-apply.md`.)

| Practice | Implements | Files | Status | Last reviewed |
|---|---|---|---|---|
| `practices/context-docs-skeleton/` | 01 | 9 `docs/` skeletons + `prompts/generate-docs.md` | current | 2026-09-08 |
| `practices/agent-entry-file/` | 03 | `AGENTS.md`, `CLAUDE.md`, `CLAUDE.local.md.example`, `.claude/rules/api.md`, Cursor pointer | current | 2026-09-08 |
| `practices/hooks-and-guards/` | 02, 05 | `.claude/settings.json`, 4 hook scripts, `lefthook.yml`, variants node/python/php-wordpress | current | 2026-09-08 |
| `practices/session-state/` | 02 | `PROGRESS.json`, `/start-session`, `/end-session`, startup routine | current | 2026-09-08 |
| `practices/worktrees/` | 06 | `.worktreeinclude`, `new-worktree.sh/.ps1`, `remove-worktree.sh`, `isolation.md` | current | 2026-09-08 |
| `practices/verification/` | 05 | Playwright smoke, Hurl smoke, pytest smoke, bats, definition-of-done, harness-evals | current | 2026-09-08 |
| `practices/spec-driven/` | 04 | `specs/README.md`, `/plan-ticket`, `/develop-task`, `constitution.md`, OpenSpec quickstart | current | 2026-09-08 |
| `practices/prompt-library/` | 01, 04, 21 | meta-prompt, ask-the-expert, readme-by-index, openapi, standards-doc, `/audit`, commit skill, `/lesson`, trajectory-review | current | 2026-09-24 |
| `practices/token-savings/` | 07 | ordered checklist, MCP audit (CLI-over-MCP rule added), measurement log | current | 2026-09-24 |
| `practices/security-baseline/` | 02, 05 | secret-scan hook, MCP trust register, agentic threat model, dependency policy, injection fixture | draft | 2026-09-28 |
| `practices/llm-api-calls/` | 10 | `llm_call_skeleton.py` (one client module, usage log incl. cached tokens), `system-prompt-template.md` (ten parts, static-first, 12-point checklist), `failure-modes-and-mitigations.md`, `provider-selection-checklist.md`, `context-budget.md` | draft | 2026-09-27 |
| `practices/context-management/` | 11 | `context-budget-and-triggers.md`, `compaction-policy.md`, `compaction_skeleton.py`, `context-failure-modes.md`, `context-store-decision.md`, `context-metrics-and-evals.md` | draft | 2026-09-27 |
| `practices/llm-gateway/` | 12 | `routing-policy.md`, `gateway_config.yaml` (LiteLLM shape), `fallback-approval.md`, `model-registry.md`, `streaming-pipeline.md`, `tracing-otel.md`, `semantic-cache-decision.md` | draft | 2026-09-30 |
| `practices/agent-patterns/` | 21 | decision checklist, patterns catalogue, agent-loop skeleton, tool-definition template + 12-point checklist, tool-transport decision table (CLI/MCP/skill/RAG/memory + auth ladder), agentic-RAG skeleton | draft | 2026-09-24 |
| `practices/_template/` | — | README template for new practices | — | — |

## Decisions

| # | File | Status |
|---|---|---|
| 0001 | `decisions/0001-knowledge-base-structure.md` — single local KB consulted by pointer | accepted |
| 0003 | `decisions/0003-applicability-by-facts.md` — practices declare `kind` + `applies-when` over the fact vocabulary in `practices/facts.md`; facts inferred from the repo; no profile schema, grammar, rigor levels or risk formula | accepted |
| 0005 | `decisions/0005-contract-first-practices-and-stacks.md` — a practice is a contract (structured Verify) + stack-sensitive points + one Python reference (`reference-status`) + an implementation prompt; no speculative ports, fifteen-line stack-notes instead; variants authored by the KB from field reports; the security guard is one fail-closed artefact; TypeScript not promised until a variant exists; two-arm Laravel experiment before module 4 is routed | accepted |
| 0004 | `decisions/0004-day-one-for-blank-and-existing-repos.md` — two entry doors (blank repo: planned facts + bootstrap; existing repo: inferred facts + audit), one router (`scripts/applies.py` as authority); safety facts select `security-baseline` (full) and `verification/dry-run-and-approval.md`; practices promoted by adoption; new practices routed only after the previous module passed Verify in a real repo | accepted |
| 0002 | `decisions/0002-market-scan-protocol-and-media-registry.md` — fixed market-scan protocol; registry of every video/podcast considered; new scans only look at new items | accepted |

## Playbooks

| File | Purpose |
|---|---|
| `playbooks/adopt-variant.md` | Turn a field report from a real repo into a field-tested variant + an adoptions row + promotion of the practice (the only path for consumer code into the KB; decision 0005 §7) |
| `playbooks/adopt-kb-in-a-repo.md` | Make a repo point to this KB (Windows-safe, no symlinks) |
| `playbooks/audit-repo-against-kb.md` | (after `which-practices-apply.md`) Inventory → score → findings → plan → stop for approval |
| `playbooks/evaluate-new-material.md` | **superseded** (2026-09-28) by the impact table in `ingest-new-source.md` step 2b; its scoring rubric was folded there. Kept for history |
| `playbooks/ingest-new-source.md` | Turn raw material into a source entry + **impact table** (confirms/refines/new/contradicts/skip/park) + only the principle/practice updates the table says — the single protocol for any external information |
| `playbooks/publish-change.md` | Ship one improvement: check → branch → commit → push → merge → delete branch (`scripts/kb-check.sh`, `scripts/kb-publish.sh`, `/publish`) |
| `playbooks/which-practices-apply.md` | Entry point for an **existing** repo (blank repos: bootstrap, to be created): infer the facts with evidence → confirm in one screen → applies / skipped with reasons → hand to the audit. Worked examples for Martin's four project shapes |
| `playbooks/scan-market-for-module.md` | For one course module: search YouTube + podcasts with Apify, select by authority, transcribe, log what was considered/selected/discarded, update `sources/scan-log.md` |

## Templates

`practices/facts.md` (applicability vocabulary: 14 facts, sources inferred/planned/asked, routing fact, ordering rule) · `practices/adoptions.md` (every adoption with its field report and cost — the KB's evidence) · `templates/field-report.md` (what an adopting agent reports; numbers mandatory) · `templates/source-entry.md` · `templates/principle.md` · `templates/decision.md` · `templates/open-spec-user-story.md` (with SSO sign-up/login worked examples)

## Scripts

`scripts/kb-sync.sh` — is this copy in sync with `origin/main`? (run first; `--pull` fast-forwards when only behind) · `scripts/kb-check.sh` — self-verification (frontmatter, index coverage, links, applicability fields + vocabulary, placeholders) · `scripts/kb-publish.sh` — branch/commit/push/merge/cleanup · `scripts/scan-filter.py` — drop already-registered media from a new scan result · `scripts/written-filter.py` — same for written sources (URLs) · `scripts/applies.py` — which practices apply for a set of facts (helper + consistency check of the playbook's worked shapes)

## Skills

`skills/README.md` — what skills are and the rules · `skills/apply-ai-engineering-kb/SKILL.md` — Agent-Skills-format entry point; copy to `~/.claude/skills/` to make it global · `practices/prompt-library/commit-skill/SKILL.md` — commit procedure

## Topic map

| Topic | Principle (why) | Practice (how) | Sources |
|---|---|---|---|
| AI Champion / agentic engineer / harness engineer roles | `00-glossary.md` | — | workshop §3.1, video A |
| Context docs, standards, workflow, definition of done | `01-context-engineering.md` | `context-docs-skeleton/` | workshop §3.3, videos B/D; research §3.1, §3.4 |
| Five harness areas, primitives, hooks, ratchet | `02-harness-engineering.md` | `hooks-and-guards/`, `session-state/` | workshop §3.4, video B; research §3.1–3.3, §3.8 |
| CLAUDE.md / AGENTS.md design, rules, imports | `03-agent-instruction-files.md` | `agent-entry-file/` | research §3.2, §3.7; workshop §3.2 |
| OpenSpec / Spec-Kit / Superpowers / Spec-Boot; ask-the-expert; plan mode | `04-spec-driven-development.md` | `spec-driven/` | workshop §3.4, videos C/D |
| Tests, e2e, Playwright, Stop hooks, evals | `05-verification-loops.md` | `verification/`, `hooks-and-guards/` | workshop §3.6, video D; research §3.2 |
| Security: secrets, dependencies, prompt injection, MCP trust | `02-harness-engineering.md` | `security-baseline/` (draft) | research §3.2; workshop §3.2, videos C/D |
| Worktrees, parallel sessions, subagents | `06-parallel-agents-and-worktrees.md` | `worktrees/` | workshop §3.4 |
| rtk, codegraph, caveman, ponytail, Headroom, routing | `07-token-economy.md` | `token-savings/` | workshop §3.5 |
| Opus/Sonnet/Gemini/Codex by phase | `08-model-selection.md` | `context-docs-skeleton/docs/workflow.md` §3 | workshop §3.2, video C |
| MCP servers (Context7, Playwright, Sentry, Snyk, Jira/Notion, Figma) | `02-harness-engineering.md`, `01-context-engineering.md` | `token-savings/mcp-audit.md` | workshop §3.2, videos C/E |
| Prompt techniques (meta-prompt, ask-the-expert, one-shot index, audit, lesson→rule) | `04-spec-driven-development.md`, `01-context-engineering.md` | `prompt-library/` | workshop §3.2, videos C/D |
| LLM API call structure, prompt structure and iteration, tokens / context window / prompt caching, reasoning models, provider selection, model failure modes | `10-llm-api-fundamentals.md` | `llm-api-calls/` | s1 digest `sources/2026-09-27-s01-llm-setup-digest.md` |
| Runtime context management: window budget, compaction, offloading, sub-agent isolation, prompt caching / KV cache economics, long context vs CAG vs RAG, context failure modes | `11-runtime-context-management.md` | `context-management/` | s2 digest `sources/2026-09-27-s02-context-caching-digest.md` |
| LLM gateway layer: routing, fallback, retries, cooldown, timeouts, capacity tiers, keys, model registry, streaming (SSE, pipeline stages), OTel GenAI tracing, semantic caching | `12-llm-gateway-layer.md` | `llm-gateway/` | s3 digest `sources/2026-09-30-s03-wrappers-digest.md` |
| How this KB is structured | `09-knowledge-base-design.md` | `practices/README.md` | research (all) |
| Agents: workflow vs agent, minimal loop, tool design, CLI/MCP/skill/RAG/memory, agentic RAG | `21-agent-design-and-tools.md` | `agent-patterns/`, `prompt-library/trajectory-review.md` | s12 digest §3, impact table §6 |

## Open actions (from sources)

- [ ] `practices/security-baseline/`: answer its open questions (secret scanner, injection eval, MCP trust policy, supply-chain rule) and ingest a dedicated security source → promote to `current`.

- [ ] Workshop homework 1: update each repo's technical context docs → run `audit-repo-against-kb.md` per repo.
- [ ] Workshop homework 2: draft the SSO open spec (sign-up, login) in one repo → `templates/open-spec-user-story.md`.
- [ ] Try `rtk` for a week; record results as a source.
- [ ] Try OpenSpec on one small AI SDR change; record results.
- [ ] Read METR and Faros originals; annotate workshop entry §4.
- [ ] Read Anthropic *Building Effective Agents* / *Writing Effective Tools*; add sources.
- [ ] Not captured from the workshop: Vimeo intro clip, attached presentation `.mp4`, Faros PDF, ~26 images.
