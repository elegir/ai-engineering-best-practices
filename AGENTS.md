# AGENTS.md — entry point for coding agents

You are reading Martin Weidemann's **AI Engineering Knowledge Base**. It is a reference library, not an application. There is nothing to build or run here. Your job when you are pointed at this folder is one of three things:

1. **Consult** — answer "what is the current best practice for X?" by reading `principles/` first (current, distilled), then `sources/` (dated evidence) only if you need the reasoning or the original wording.
2. **Apply** — evaluate another repository against these practices and propose (not silently execute) a plan. Use `playbooks/audit-repo-against-kb.md`; each gap maps to a folder in `practices/` with ready-to-copy files, an "applies when / does not apply when" test, and verification steps.
3. **Ingest** — turn new raw material (a transcript, an article, notes) into a dated source entry with an **impact table** and update only what the table says. Use `playbooks/ingest-new-source.md`. The goal is to improve the KB, not to add everything: expect a third of any source to be "confirms" (record the review), a fifth to be "park" or "skip".
4. **Scan** — for one topic or course module, find the market's most authoritative videos and podcasts, select, transcribe and log them. Use `playbooks/scan-market-for-module.md` (the protocol; decision `decisions/0002-market-scan-protocol-and-media-registry.md`); progress per module is tracked in `sources/scan-log.md`, and every item ever considered — including discarded ones — is in `sources/media-registry.json`. Never re-examine a registered item; run `scripts/scan-filter.py` on every new search result.

## Where things are

- `INDEX.md` — chronological list of every source entry and a topic → file map. Start here for orientation.
- `principles/` — one file per topic: the *what* and *why*. Each has frontmatter with `status` (`current` | `draft` | `superseded`) and `last-reviewed`. **Only trust files whose status is `current`.**
- `practices/` — one folder per practice: the *how*, with copyable files (docs skeletons, `AGENTS.md` model, hook scripts, `PROGRESS.json`, worktree scripts, smoke tests per app type, spec commands, prompts, token checklist) and stack variants. Start at `practices/README.md`. Copy and adapt; never copy blindly.
- `sources/YYYY-MM-DD-slug.md` — immutable digests. Never edit the body of an existing source; add a new one.
- `decisions/NNNN-slug.md` — decisions about how Martin's repos work. Respect any with status `accepted`.
- `playbooks/` — procedures. Follow them literally. `ingest-new-source.md` (add knowledge) and `publish-change.md` (ship it) are the two this folder runs on itself; `adopt-kb-in-a-repo.md` and `audit-repo-against-kb.md` are for agents in *other* repos.
- `scripts/` — `kb-check.sh` (the KB's own verification) and `kb-publish.sh` (branch/commit/push/merge/cleanup).
- `templates/` — copy these when creating new entries.
- `CONVENTIONS.md` — formatting rules for anything you write here.

## Rules when writing into this folder

- Write in **English**. Long-form, digested, explicit: assume the reader has no background. Prefer full sentences and explanations over terse bullets.
- Every new file gets the frontmatter defined in `CONVENTIONS.md`.
- Date everything. Never write "recently" or "the latest version"; write the date and the version.
- Cite sources by relative path (e.g. `sources/2026-09-08-lidr-workshop-harness-engineering.md`) or URL. No unsourced claims presented as fact; mark opinions as opinions.
- When a new source contradicts a principle, do **not** overwrite the old text silently. Add a "Change log" line to the principle explaining what changed, why, and which source triggered it. If the old advice is fully obsolete, set its status to `superseded` and point to the replacement.
- Update `INDEX.md` in the same change.
- Never delete files. Mark them superseded.
- **Publish every improvement through `playbooks/publish-change.md`**: `bash scripts/kb-check.sh` then `bash scripts/kb-publish.sh <slug> "<message>"` (branch → commit → push → merge to `main` → branch deleted). Never commit by hand on `main`; never `--no-verify`.

## Rules when applying this knowledge to another repo

- Read the target repo before recommending anything. Recommendations must reference actual files, commands and gaps in *that* repo.
- Investigation before implementation: produce a written plan (what, why, which principle, expected effort) and stop for Martin's approval before changing files. One problem per prompt.
- Prefer mechanical enforcement (hooks, linters, tests, CI) over adding more prose to instruction files. Principle: `principles/05-verification-loops.md`; files: `practices/hooks-and-guards/`, `practices/verification/`.
- For every gap, use the matching `practices/<name>/`: check "Applies when / Does not apply when", pick the stack variant, replace every `<<PLACEHOLDER>>`, run its "Verify" section.
- Keep the target repo's `CLAUDE.md` / `AGENTS.md` short and pointer-based. Principle: `principles/03-agent-instruction-files.md`.
- Explain steps simply, one at a time, assuming Martin is not going to run anything he does not understand.

## Quick topic map

| I need to… | Why (principle) | How (practice, copyable files) |
|---|---|---|
| understand the vocabulary (harness, context, loop, SDD, AI Champion…) | `principles/00-glossary.md` | — |
| give an agent the right project context | `principles/01-context-engineering.md` | `practices/context-docs-skeleton/` |
| build the environment around the agent (tools, state, sensors) | `principles/02-harness-engineering.md` | `practices/hooks-and-guards/`, `practices/session-state/` |
| write or fix a `CLAUDE.md` / `AGENTS.md` | `principles/03-agent-instruction-files.md` | `practices/agent-entry-file/` |
| work spec-first (OpenSpec, Spec-Kit, Superpowers, Spec-Boot) | `principles/04-spec-driven-development.md` | `practices/spec-driven/`, `templates/open-spec-user-story.md` |
| make agents verify their own work (tests, hooks, e2e) | `principles/05-verification-loops.md` | `practices/verification/`, `practices/hooks-and-guards/` |
| run several agents in parallel safely (worktrees) | `principles/06-parallel-agents-and-worktrees.md` | `practices/worktrees/` |
| spend fewer tokens | `principles/07-token-economy.md` | `practices/token-savings/` |
| pick a model for a task | `principles/08-model-selection.md` | (policy table in `practices/context-docs-skeleton/docs/workflow.md` §3) |
| reuse the high-leverage prompts (meta-prompt, ask-the-expert, audit, lesson→rule) | `principles/01-context-engineering.md`, `principles/04-spec-driven-development.md` | `practices/prompt-library/` |
| structure a knowledge base like this one | `principles/09-knowledge-base-design.md` | — |
| decide workflow vs agent, build the minimal loop, design tools, choose CLI/MCP/skill, agentic RAG | `principles/21-agent-design-and-tools.md` (draft) | `practices/agent-patterns/`, `practices/prompt-library/trajectory-review.md` |
