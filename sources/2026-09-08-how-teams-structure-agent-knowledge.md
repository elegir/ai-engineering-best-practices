---
title: "Research digest — how experienced teams structure knowledge for coding agents (and why this KB is shaped the way it is)"
type: source
status: current
date: 2026-09-08
tags: [knowledge-base-design, agents-md, agent-skills, harness-engineering, documentation]
sources:
  - https://openai.com/index/harness-engineering/
  - https://nyosegawa.com/en/posts/harness-engineering-best-practices-2026/
  - https://github.com/ai-boost/awesome-harness-engineering
  - https://blog.sigplan.org/2026/04/21/repositories-are-human-agent-knowledge-factories/
  - https://ravichaganti.com/blog/documentation-stack-for-ai-agents/
  - https://agentskills.io/home
  - https://code.claude.com/docs/en/memory
  - https://www.lidr.co/blog/que-es-harness-engineering/
supersedes: null
superseded-by: null
---

# How experienced teams structure knowledge for coding agents

## 1. Context

Before creating this knowledge base, a web survey was done on 2026-09-08 to answer one question: *when professional teams accumulate engineering know-how that AI agents must consume across many repositories, how do they organize it?* The sources are OpenAI's write-up of its Codex team's practices, a widely-shared 2026 practitioner guide on harness engineering for Claude Code/Codex users, the `awesome-harness-engineering` curated list, a SIGPLAN blog essay on repositories as "knowledge factories", a documentation-stack overview, the Agent Skills open standard, the Claude Code memory documentation, and LIDR's own harness article. This entry records what they agree on, where they differ, and which of their recommendations this KB adopted.

## 2. One-paragraph summary

The pros converge on a small set of ideas. Knowledge for agents lives **in Markdown, in git**, next to (or reachable from) the code, because that is the only format every agent reads natively and the only one that versions and diffs. The **entry-point file is short and pointer-based** (an `AGENTS.md`/`CLAUDE.md` of roughly 50–200 lines that says *where* to look, not *what everything is*), and depth lives in a `docs/` tree loaded on demand — the same "progressive disclosure" that the Agent Skills standard formalizes. Content is separated by **how it ages**: immutable, dated records (ADRs, meeting digests) versus living references versus executable artifacts (tests, linters, hooks), because agents cannot tell stale prose from current truth. Each fact lives in **exactly one place** and everything else links to it. And whatever can be **enforced mechanically** (hooks, linters, CI) should be, rather than written as prose the agent may ignore.

## 3. Detailed digest

### 3.1 OpenAI — "Harness engineering" (Codex team)

The Codex team treats the repository as the **system of record** for everything an agent may need: "anything not discoverable in the repository doesn't exist for the agent" — decisions in Slack, Google Docs or people's heads are invisible. Their structure: a lightweight `AGENTS.md` (~100 lines) that works as a **table of contents**, and a `docs/` directory that holds the authoritative material organized by category — `design-docs/` (indexed design decisions), `exec-plans/` (active and completed work), `generated/` (auto-produced schemas), `product-specs/`, and topic guides such as `FRONTEND.md`, `RELIABILITY.md`, `SECURITY.md`. They explicitly rejected the monolithic instruction file for three reasons: **context scarcity** (it burns the window), **guidance decay** (it rots), and **verification difficulty** (you cannot check a wall of prose). "Give Codex a map, not a 1,000-page instruction manual."

Two enforcement mechanisms keep it honest: **linters and CI jobs validate that documentation is current, cross-linked and correctly structured**, and a recurring **"doc-gardening" agent** scans for obsolete content and opens corrective PRs. Architecture is enforced the same way — fixed layers per domain (Types → Config → Repo → Service → Runtime → UI) with validated dependency direction, custom linters encoding "taste invariants" (structured logging, naming, file-size limits), and structural tests. "Enforce boundaries centrally, allow autonomy locally." Because agents replicate existing patterns including bad ones, they run background "garbage-collection" agents that detect drift and open small PRs reviewable in under a minute. Their headline numbers: three engineers → ~1,500 merged PRs (~3.5/engineer/day) over ~1M lines. Their meta-insight: "the discipline shows up more in the scaffolding than in the code."

### 3.2 Practitioner guide — "Harness engineering best practices for Claude Code / Codex users" (2026)

The most concrete source, and the one this KB borrows most conventions from.

**Design for rot.** Agents treat all discoverable text as equally authoritative. So: keep *executable* artifacts in the repo (code, tests, linter configs, schemas, CI) and **ADRs**, which resist rot because they are immutable and carry a status (Accepted / Superseded / Deprecated) an agent can read structurally. Prose describing *current* system state (design overviews, hand-written API descriptions) inevitably falls behind. Research cited: "stale information the agent can find in the repo is indistinguishable from the latest truth", and performance degrades for all frontier models as context grows. Use tests to express specs — "tests can't lie when you run them".

**Mechanism over prompts.** "Whenever a deterministic tool can do the job, use it." Four hook patterns for Claude Code: *safety gates* (PreToolUse; block `rm -rf`, `.env` edits; exit code 2 returns the reason to the agent), *quality loops* (PostToolUse; run formatter/linter after edits and return violations as `hookSpecificOutput.additionalContext` JSON), *completion gates* (Stop hook; tests must pass before the agent may declare done), *observability*. Push checks to the fastest layer: PostToolUse (ms) > pre-commit (s) > CI (min) > human review (hours). Protect linter configs from the agent (PreToolUse block on `.eslintrc`, `pyproject.toml`, etc.) and ban `git commit --no-verify`. Write linter error messages as fix instructions (`WHY:` linking the ADR, `FIX:`, `EXAMPLE:`), because agents cannot ignore CI failures but can ignore docs. The "archgate" pattern pairs each ADR with an executable rule file.

**AGENTS.md / CLAUDE.md as a pointer.** Target **under 50 lines at root**; the official "<200 lines" is an upper bound, not a target — compliance drops as instruction count grows. Contents: routing ("run `npm test`", "ADRs live in `/docs/adr/`"), prohibitions each pointing to an ADR or rule, minimum build/test/deploy commands. *Not* contents: system-state explanations, tech-stack descriptions (agents read `package.json`), verbose style guides (delegate to linters). Ask of every line: "would removing this cause mistakes?" Pointer design has a bonus: broken pointers fail loudly; descriptive docs rot silently.

**Separate planning from execution**; one feature at a time; require end-to-end test execution before "done" (browser automation for web; accessibility tree over screenshots for token efficiency — Playwright CLI ~27K tokens vs Playwright MCP ~114K per the guide; Hurl for HTTP APIs; bats for CLIs).

**Session state.** Standardize the startup routine (check working dir, read git log and a progress file, pick the next task, sanity-check the dev server). Use git log as the "what happened" record; use **JSON rather than Markdown for progress/feature lists** because models are less likely to mangle JSON.

**Minimum Viable Harness roadmap.** Week 1: pointer-based instruction file, pre-commit hooks (Lefthook), PostToolUse formatter, first ADR. Weeks 2–4: add a test or linter rule every time the agent errs; plan → approve → execute; introduce an E2E tool; tests as the Stop-hook condition. Months 2–3: custom linters referencing ADRs; replace descriptive docs with tests and ADRs; PreToolUse safety gates. Month 3+: garbage-collection processes; multiple agents; measure PRs/day, rework rate, review-comment rate.

**Anti-patterns**: prompt-only enforcement; accumulating explanatory docs; bloated instruction files (>1,000 lines "burn context before the first question"); agent-only infrastructure (Stripe: "build excellent developer infrastructure; agents benefit automatically"); scaling agent count before the harness works.

### 3.3 `awesome-harness-engineering` (curated list)

Defines harness engineering as designing the scaffolding — context delivery, tool interfaces, planning artifacts, verification loops, memory systems, sandboxes — around an agent, on the premise that "every component exists because the model can't do it alone". Its taxonomy of design primitives (agent loop, planning/decomposition, context delivery & compaction, tool design, skills & MCP, permissions, memory & state, orchestration, verification & CI, observability, debugging/DX, human-in-the-loop) is a useful checklist for auditing a repo's harness. Foundational references it lists: OpenAI's harness-engineering post, Anthropic's *Building Effective Agents*, *Harness Design for Long-Running Apps*, *Writing Effective Tools for Agents*, Martin Fowler's synthesis, Microsoft's Azure SRE Agent case study (35k+ incidents; moved from 100+ tools to filesystem-based context, raising "intent met" from 45% to 75% on novel incidents). Key claims: "the model is the engine; the harness is the car"; for the same model, swapping the harness moved SWE-bench by 22 points while swapping the model moved it by 1 (as cited by the practitioner guide); and — importantly — as models improve, harness design matters *more*, because better models expose bottlenecks that weaker models masked. Design components "to fade away", not calcify.

### 3.4 SIGPLAN — "Repositories are human/agent knowledge factories" (2026-04)

Academic framing of the same shift: repositories must become "containers and generators of knowledge" for agents while staying human-reviewable. Proposes a **four-level hierarchy**: Level 0 `AGENTS.md` (dispatcher: build/lint commands, universal conventions, injected every session); Level 1 `agent-reference.md` (architecture overview, data schemas with JSON examples, CLI syntax); Level 2 `specs/` (formal specifications in RFC 2119 MUST/SHOULD/MAY language defining component contracts); Level 3 source code and tests as ground truth. Principles: **single source of truth** ("each fact lives in exactly one document; all other references are links"), **scoped instructions** injected only when the agent edits matching paths, **specification-first development** (write specs and conformance tests before implementation). Six failure modes: inaccessible knowledge, stale duplicates, monolithic prompts, unchecked assumptions, stale derived artifacts, premature optimization. Why it matters: "agents lack the social feedback mechanisms" that let human teams catch these.

### 3.5 Documentation stack for AI agents

A layered menu rather than a single answer: `llms.txt` at a site root for external discovery; `AGENTS.md` at the repo root for onboarding ("tribal knowledge that would normally be passed down in Slack threads"); Markdown-first docs (`.md` endpoints beside HTML — "pure signal"); OpenAPI specs for machine-readable contracts; MCP servers for live data; `SKILL.md` files for procedural, multi-step knowledge loaded progressively; RAG pipelines only for unstructured internal material. Choose by need: internal guidelines → `AGENTS.md`; procedures → skills; private institutional knowledge → RAG. No single layer suffices.

### 3.6 Agent Skills open standard (agentskills.io)

A skill is a folder with a `SKILL.md` (YAML frontmatter with at least `name` and `description`, then instructions) plus optional `scripts/`, `references/`, `assets/`. **Progressive disclosure in three stages**: *discovery* (only name + description loaded at startup), *activation* (full `SKILL.md` read when a task matches), *execution* (bundled files loaded as needed). Originally developed by Anthropic, released as an open standard, adopted by 40+ agent products including Claude Code, Cursor, Codex, Copilot, Gemini CLI, OpenCode, Junie, Kiro, Goose. This is the portable format for "how to do X" knowledge that must work across tools.

### 3.7 Claude Code memory docs (for the cross-repo mechanics)

Facts that matter for consulting a shared KB from other repos on Windows:

- `CLAUDE.md` loads from the working directory and every directory above it; subdirectory files load on demand. Target **<200 lines**; longer files reduce adherence. `/doctor` proposes trims; it cuts content Claude can derive from the codebase.
- `@path` imports pull other files in **at launch** (they still consume context); relative paths resolve relative to the importing file; max depth 4; an import outside the working directory triggers an approval dialog once, and in Cowork desktop sessions such external imports are skipped.
- Claude Code reads `CLAUDE.md`, not `AGENTS.md`; bridge with `@AGENTS.md` (on Windows, symlinks need admin/Developer Mode, so use the import).
- `.claude/rules/*.md` with `paths:` frontmatter loads only when matching files are touched — the "scoped instructions" pattern.
- `--add-dir` plus `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` loads memory files from another directory.
- CLAUDE.md is *context, not enforcement*; to block an action use a PreToolUse hook.
- Auto memory (`~/.claude/projects/<project>/memory/MEMORY.md` + topic files) is per-repo and machine-local — not a substitute for a shared KB.

### 3.8 LIDR — "Qué es harness engineering"

Adds a role comparison: *Harness Engineer* (agent execution environment; "what part of the infrastructure is failing?"), *Agentic Engineer* (orchestrating agents in workflows), *AI Engineer* (AI-centric product architecture), *MLOps Engineer* (model lifecycle). Daily practice is a **ratchet**: when an agent fails, design a control that prevents recurrence instead of fixing by hand — maintain `AGENTS.md`, write preventive hooks, build eval suites for CI, configure observability (decisions, token costs, failure points), deploy bounded sub-agents.

## 4. Claims worth checking

- The "22 points from the harness vs 1 from the model" SWE-bench claim is cited second-hand; find the primary.
- Token counts for Playwright MCP vs CLI vs agent-browser are the guide's measurements on its own tasks.
- OpenAI's PR throughput numbers are self-reported.

## 5. What is contested

- **How much prose to keep.** The practitioner guide says almost none (tests + ADRs + pointers); OpenAI and LIDR keep substantial `docs/` prose but police it mechanically. This KB is *itself* prose, so it adopts the OpenAI/LIDR position with the guide's safeguards: dated entries, status fields, single source of truth, an index, and a "never silently overwrite" rule.
- **Markdown vs JSON for state.** The guide prefers JSON for progress files. Reasonable, but irrelevant for a knowledge base; noted for the playbooks.
- **Where the KB should live relative to code.** The guide suggests keeping README-style docs *outside* the grep scope of the agent's working repo to avoid rot contaminating it. That is exactly why this KB is a **separate sibling folder** consulted by pointer, not copied into each repo.

## 6. Implications — what this KB adopted

| Recommendation | Source | How it shows up here |
|---|---|---|
| Short pointer-style entry file | practitioner guide, OpenAI | `AGENTS.md` (~60 lines), `CLAUDE.md` = `@AGENTS.md` |
| Deep `docs/` organized by category, indexed | OpenAI | `principles/`, `sources/`, `decisions/`, `playbooks/` + `INDEX.md` |
| Immutable dated records with status | practitioner guide (ADRs), SIGPLAN | `sources/` never edited; `decisions/` with status; principles carry `status` + `last-reviewed` |
| Single source of truth, link don't copy | SIGPLAN | `CONVENTIONS.md` §6–7; other repos point to this folder instead of copying |
| Progressive disclosure / skills | agentskills.io | `skills/apply-ai-engineering-kb/SKILL.md` |
| Mechanical enforcement over prose | practitioner guide, OpenAI | `principles/05-verification-loops.md`; audit playbook recommends hooks/linters before adding rules |
| Cross-repo consumption on Windows without symlinks | Claude Code docs | `playbooks/adopt-kb-in-a-repo.md` uses a prose pointer + optional `@` import |
| Ratchet: every failure becomes a rule/test | LIDR, Boris Cherny (see workshop entry) | `playbooks/ingest-new-source.md` includes "lessons from failures" as a source type |

## 7. Actions

- [x] Structure created per the table above (`decisions/0001-knowledge-base-structure.md`).
- [ ] Read Anthropic's *Building Effective Agents* and *Writing Effective Tools for Agents* and add source entries.
- [ ] Try the "doc-gardening" idea: a monthly agent run over this KB checking for principles whose `last-reviewed` is older than 90 days.
