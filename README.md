# AI Engineering Knowledge Base

A single, local, version-controlled folder that accumulates everything Martin learns about building software with AI agents: workshops, articles, talks, experiments, and the decisions that come out of them. Every other repo in `Local Coding/` can point an agent here and ask: *"read the knowledge base and tell me how to apply it to this repo."*

The discipline this folder covers goes by several names depending on who is talking: **AI engineering**, **harness engineering**, **context engineering**, **agentic engineering**, **spec-driven development (SDD)**. They are layers of the same thing (see `principles/00-glossary.md`). The short version: **Agent = Model + Harness**. The model is rented. The harness — the instructions, tools, tests, hooks, sandboxes and workflows around it — is the part you own and the part that decides whether an agent produces production-grade work. This knowledge base is where the harness know-how lives.

## How the folder is organized

Three kinds of content, deliberately kept apart because they age differently:

| Folder | What it holds | How it ages |
|---|---|---|
| `sources/` | Dated, long-form digests of *where knowledge came from*: one file per workshop, article, talk or experiment. Written once, never rewritten. Filename starts with the date (`2026-09-08-...`). | Immutable. A source is a snapshot of what was said on that date. |
| `principles/` | The *distilled, current* best practices by topic — the **what and why**. Each file is a living document with a `status` and a `last-reviewed` date and cites the sources it was built from. | Living. Updated whenever a new source changes the recommendation. Old advice is marked `superseded`, not deleted. |
| `practices/` | The **how**: one folder per applicable practice with ready-to-copy files (docs skeletons, entry-file model, hook scripts, progress file, worktree scripts, smoke tests per app type, spec commands, prompt library, token checklist), stack variants, an "applies when / does not apply when" test, and verification steps. This is what agents in other repos actually copy and adapt. | Living, same rules as principles. |
| `decisions/` | Architecture-Decision-Record-style notes on *what Martin has decided* his repos will do (e.g. "all repos use worktrees per ticket"). Numbered, dated, with a status. | Append-only. A decision is replaced by a newer decision that supersedes it. |
| `playbooks/` | Step-by-step procedures an agent (or a person) can execute, e.g. "audit this repo against the knowledge base". | Living, versioned. |
| `templates/` | Blank templates for each kind of entry, so new entries stay consistent. | Rarely changes. |
| `skills/` | An Agent-Skills-format skill (`SKILL.md`) that any compatible coding agent (Claude Code, Cursor, Codex, Copilot…) can load to consult this knowledge base. | Rarely changes. |

Entry points:

- `AGENTS.md` — the file an agent should read first. Short, pointer-based. `CLAUDE.md` just imports it.
- `INDEX.md` — chronological log of every source entry plus a topic index. Update it every time you add a file.
- `CONVENTIONS.md` — the rules for writing entries (frontmatter, tags, dating, how to mark stale advice).

## How to use it from another repo

The design goal is that any repo in `Local Coding/` can consult this folder **without copying it**, and that the knowledge base stays the single source of truth.

1. In the other repo's `CLAUDE.md` (or `AGENTS.md`) add a pointer, not a copy:

   ```markdown
   ## Shared engineering knowledge base
   Martin's AI-engineering best practices live in `../ai-engineering-best-practices/` (sibling folder).
   Before proposing changes to tooling, agent instructions, testing strategy, specs or workflow,
   read `../ai-engineering-best-practices/AGENTS.md` and follow the relevant playbook.
   ```

2. Then, inside that repo, ask the agent: *"Run the playbook `../ai-engineering-best-practices/playbooks/audit-repo-against-kb.md` on this repo and propose a plan."* The plan maps each gap to a `practices/` folder; after approval the agent copies and adapts those files one item at a time.

3. Optionally, copy `skills/apply-ai-engineering-kb/` into `~/.claude/skills/` so the skill is available in every project on this machine.

The full procedure, including Windows-specific notes (no symlinks needed), is in `playbooks/adopt-kb-in-a-repo.md`.

## How to add new knowledge

Every time Martin attends a workshop, reads something worth keeping, or runs an experiment:

1. Create `sources/YYYY-MM-DD-short-slug.md` from `templates/source-entry.md`. Write it **long and digested**: what was said, what it means, why it matters, what is contested, and what concrete actions come out of it. Assume the reader knows nothing.
2. Update the relevant `principles/*.md` files (or create a new one). Change `last-reviewed`, cite the new source, and if the recommendation changed, say what changed and why.
2b. If the source brings something *applicable* (a config, a script, a prompt, a template), add it to the matching `practices/<name>/` folder — or create a new practice from `practices/_template/`. A principle without a practice is advice; a practice is what other repos can actually adopt.
3. If a decision was made, add `decisions/NNNN-slug.md`.
4. Add one line to `INDEX.md`.
5. Publish: `bash scripts/kb-check.sh` (the KB verifies itself) then `bash scripts/kb-publish.sh <slug> "kb: add 2026-09-08 LIDR harness workshop"` — creates a branch, commits, pushes, merges into `main`, deletes the branch. Details: `playbooks/publish-change.md`.

The fastest way to do steps 1–5 is to hand an agent the raw material (transcript, notes, links) and ask it to run `playbooks/ingest-new-source.md` followed by `playbooks/publish-change.md`.

The repository lives on GitHub (https://github.com/elegir/ai-engineering-best-practices); `main` is always the current state, every improvement is one short-lived `kb/<slug>` branch merged and deleted by the publish script.

## Why this shape and not a wiki / Notion / a single big file

This is what the current "pros" converge on (details and sources in `sources/2026-09-08-how-teams-structure-agent-knowledge.md`):

- **Markdown in a git repo** is the format every coding agent can read natively; it diffs, it versions, it works offline, and it can be grepped by the agent.
- **A short pointer file (`AGENTS.md`) plus deep `docs/`** beats one giant instruction file. Agents follow short instruction files more reliably; long ones degrade adherence. OpenAI's own Codex team describes AGENTS.md as "a map, not a 1,000-page manual".
- **Dated, immutable sources + living principles + append-only decisions** is the pattern that resists rot: an agent can always tell what is current (status fields, dates) versus what was true on some date.
- **Progressive disclosure**: metadata first, full content only when relevant — the same pattern the Agent Skills open standard uses. That is why `AGENTS.md` is short and links outward.
- **Single source of truth**: each fact lives in exactly one file; everything else links to it. Copies drift.

## Language

Everything in this folder is written in **English** so that agents, tools and any future collaborators read the same thing. Martin's own conversations about it can happen in Spanish; the artifacts are English.
