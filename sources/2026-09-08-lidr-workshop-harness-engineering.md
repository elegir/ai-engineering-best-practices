---
title: "LIDR workshop — De Developer a AI Champion: Harness Engineering para construir flujos agénticos reales"
type: source
status: current
date: 2026-09-08
tags: [harness-engineering, context-engineering, spec-driven-development, ai-champion, worktrees, token-economy, model-selection, verification]
sources:
  - https://lidr.notion.site/material-workshop-harness-engineering-202609
  - https://notes.granola.ai/t/86ac645f-dc67-4dcd-be4c-2487162f6943
  - https://www.lidr.co/blog/que-es-harness-engineering/
  - https://www.lidr.co/blog/como-ahorrar-tokens-en-desarrollo-de-software/
supersedes: null
superseded-by: null
---

# LIDR workshop: "De Developer a AI Champion — Harness Engineering para construir flujos agénticos reales"

## 1. Context

- **What**: a free live workshop (Spanish-language, ~90 min) given by **Álvaro Moya**, CTO & founder of **LIDR** (lidr.co), a Spanish company that trains engineering teams in AI adoption. The workshop is the public front door to their paid course *"Harness Engineering & SDD"*.
- **When**: Tuesday **2026-09-08**, 10:00 Mexico City time.
- **Who attended**: Martin Weidemann (first workshop of this kind he has attended). Audience was mostly Spanish-speaking developers and tech leads.
- **Material**: a Notion "preparation hub" with six sections (AI Champion role, the three pillars, context engineering, harness engineering, token savings, a poll on verification) and five embedded YouTube videos. Everything was captured on 2026-09-08 and is preserved verbatim in `sources/raw/2026-09-08-lidr-workshop/`: the full Notion text (`notion-preparation-hub-full-text.md`) and the five video transcripts (`yt-*.md`, extracted with Apify). Martin's Granola recording of the live session produced an automatic summary (reproduced in §8); the raw live-session transcript was not retrievable. Not captured: a Vimeo promo clip, an attached `.mp4` of Álvaro's presentation, the attached Faros AI PDF, and ~26 screenshots/diagrams.
- **Sections in this digest**: §3.1–3.8 digest the Notion hub and the live session; **§3.9 digests the five videos**, which contain material the hub only summarizes (the 5-area harness model, the "three ingredients and a golden rule" of context, the 1,000-line standards documents, the `definition of done` idea, and the prompt-generation techniques).
- **Why this matters for the knowledge base**: this is the founding entry. It gives the vocabulary (context → harness → loop), a concrete list of frameworks to choose from, and two homework items Martin took away.

## 2. One-paragraph summary

The workshop's thesis is that using an AI coding agent well is not an individual skill but a *system* you build around the model, and that a new role — the **AI Champion** — is emerging to own that system inside companies. The system has three layers: **context engineering** (what the agent knows before it acts), **harness engineering** (the tools, sandboxes, rules and automatic checks around it), and **loop engineering** (the automation that triggers, verifies and chains agent runs). The formula the speaker keeps returning to is *Agent = Model + Harness*: the model is a commodity; the harness is where teams differentiate. Practically, this means adopting a **spec-driven development** framework (OpenSpec, Spec-Kit, Superpowers, or LIDR's Spec-Boot as a context layer), running parallel agents in isolated **git worktrees**, forcing **end-to-end verification** (Playwright etc.) rather than manual review, and using a handful of open-source tools to cut token spend by 50–60%. Martin's two takeaways: rewrite his technical context documents per project following the structure shown, and draft a first "open spec" for single sign-on as user stories.

## 3. Detailed digest

### 3.1 The AI Champion role

The speaker frames the workshop around a role rather than a technique. Drawing on OpenAI Academy's "AI Champion" framework, an AI Champion is an internal employee who promotes, supports and accelerates practical AI adoption. Not necessarily IT, not necessarily a manager: a *peer advocate* whose credibility makes adoption feel normal. OpenAI distinguishes **Leaders** (strategic; governance, metrics, cross-functional alignment) from **Activators** (embedded in one team; design practical flows, coach colleagues).

LIDR narrows it for software teams: *the AI Champion builds the agentic layer and governs AI adoption in a standardized, consistent way across the team*. Concretely that means: configuring the agent's technical environment, coaching change management, and running the cycle **measure → feedback → improve → distribute** (code changes + formal training + communication such as tutorials/webinars). Today this is usually the Tech Lead.

A related role, the **Agentic Engineer**, masters the technical side (designs systems agents execute). The AI Champion adds what makes it scale: influence, leadership, change management, team training — soft skills on a solid technical base.

The Granola summary adds the speaker's framing of the **harness engineer** as sitting *above* senior/architect level, owning "the full interaction layer, not just code execution", and encompassing prompt engineering, context engineering, loop design and latency control. The profile listed: full-stack awareness (front, back, mobile, infra, CI/CD, pipelines), testing/accessibility/scalability, and an AI/ML layer (LangChain, LangGraph, orchestration frameworks such as Microsoft's agent tooling). The speaker's rough numbers: ~15–20% of developers reach a strong senior level, and fewer become champions/leads.

**Data the speaker used to justify the role** (all as cited by LIDR; not independently verified here):

- Stack Overflow 2025 survey: 92.6% of developers use an AI coding assistant at least monthly.
- GitHub Copilot: >4.7M paid subscribers (+75% YoY), deployed in 90% of the Fortune 100.
- Lightcast: developers with AI skills earn ~28% more (~$18k/year more in the US).
- McKinsey (4,500 devs, 150 companies): teams that integrate AI *well* cut routine-task time by 46%.
- **METR controlled trial**: experienced developers using AI tools were **19% slower** yet *believed* they were 20% faster. The speaker's point: perceived speed ≠ real speed without a verification system.
- **Faros AI "The Acceleration Whiplash"** (telemetry from 22,000 devs / 4,000+ teams, two years): individual productivity up (+66% epics per dev, +33.7% throughput) but downstream cost: **bugs per dev +54%, incidents per PR +242.7%, review time +441%, and 31.3% more PRs merged with no review at all.**

The interpretation: individual acceleration without team governance does not reduce work, it *redistributes* it to the phase nobody is watching. The AI Champion's job is to make the whole team use AI with the same criteria.

### 3.2 The three pillars ("TPC" methodology): Tool, Prompt, Context

LIDR's method rests on three pillars, in increasing order of importance:

1. **Tool** — which copilot/agent and how it is configured (MCPs, settings, model, memory).
2. **Prompt** — how instructions are structured.
3. **Context** — the most important today: everything that makes output align with the project's conventions.

**Tool recommendations (as of 2026-09-08):**

- Speaker's own setup: **Claude Code** as CLI (~$17/month tier mentioned) + **Cursor** as IDE (~$20/month). If only one: start with Cursor, or GitHub Copilot / Codex plugins, or OpenCode (free models, can also connect Codex — good if you already pay ChatGPT). All four have CLIs; graduate to Claude Code once comfortable in the terminal.
- **Recommended MCP servers**: for context — Atlassian (Jira/Confluence), **Context7** (up-to-date library docs), Figma (Framelink or official); for QA — **Playwright**; for errors/security — **Sentry**, **Snyk**. Configured through an `mcp.json` at OS, IDE or project level. Example shown:

  ```json
  {
    "servers": {
      "github":     { "type": "http", "url": "https://api.githubcopilot.com/mcp" },
      "playwright": { "command": "npx", "args": ["-y", "@microsoft/mcp-server-playwright"] }
    }
  }
  ```

- Other settings: Privacy mode ON, Memories ON. In Cursor, "composer 2" described as fast and reliable.

**Model selection.** The speaker's key point: brand matters less than *reasoning depth*. Knowing which tasks need deep reasoning gives both precision and token savings. His table (Anthropic / Google / OpenAI columns):

| Phase | Anthropic | Google | OpenAI | Why |
|---|---|---|---|---|
| Discovery, initial context | Sonnet | Gemini LOW/MED | — | fast, precise, no over-engineering |
| PRD / user stories | Sonnet | Gemini LOW/MED | — | short iteration loops on drafts |
| Technical design / architecture / specs | **Opus** | Gemini HIGH | Codex | reasons about trade-offs |
| Routine implementation | Sonnet | Gemini LOW/MED | — | daily driver |
| Complex implementation (legacy, refactor, cross-module) | **Opus** | Gemini HIGH | Codex | wide context, autonomous |
| Shallow review / debugging | Sonnet | Gemini LOW/MED | — | enough for 80% |
| Deep debugging / security | **Opus** | Gemini HIGH | Codex | Codex strong in terminal |
| DevOps / CI-CD / terminal | **Opus** | Gemini HIGH | **Codex** | Codex 77.3% vs Opus 65.4% on Terminal-Bench (as cited) |
| Production maintenance | Sonnet | Gemini LOW/MED | — | continuous iteration at reasonable cost |

Rule of thumb for SDD: **the top-tier model (Opus) plans and writes the specs exhaustively; the mid-tier model (Sonnet) executes the already-atomized tasks.** Speaker's provider preference: Anthropic (latest Opus for planning, Sonnet 4.6 for execution), with Codex and Gemini Pro as valid alternatives.

**Boris Cherny's Claude Code setup** (translated by LIDR from an X thread by the creator of Claude Code) — reproduced here because it is a compact list of concrete practices:

- Runs ~5 Claude Code sessions in parallel in numbered terminal tabs with system notifications, plus 5–10 more on claude.ai/code, and starts sessions from the phone.
- Uses the top model with thinking for everything: needs less steering, so it is usually faster overall.
- **One shared `CLAUDE.md` per repo, committed to git, edited several times a week by the whole team. Every time Claude does something wrong, the rule goes into `CLAUDE.md`.** During code review he tags `@.claude` on colleagues' PRs to add to `CLAUDE.md` as part of the PR (via the Claude Code GitHub Action). He calls this their version of "Compounding Engineering".
- Most sessions start in **Plan mode**; iterate on the plan, then switch to auto-accept edits and let Claude one-shot it. "A good plan is really important."
- **Slash commands** (`.claude/commands/`, committed) for every inner-loop workflow done many times a day, e.g. `/commit-push-pr`, using inline bash to pre-compute git state.
- **Subagents** for recurring workflows: `code-simplifier` (after Claude finishes), `verify-app` (end-to-end test instructions).
- **PostToolUse hook** to format code (handles the last 10% that would fail CI).
- Does *not* use `--dangerously-skip-permissions`; instead pre-allows safe bash commands via `/permissions`, committed in `.claude/settings.json`.
- Claude uses all his tools via MCP: Slack, BigQuery (`bq` CLI), Sentry. `.mcp.json` committed and shared.
- For long tasks: ask Claude to verify with a background agent at the end, or a **Stop hook**, or the `ralph-wiggum` plugin; run in a sandbox with permissions relaxed.
- **"The single most important thing: give Claude a way to verify its work.** With that feedback loop, quality doubles or triples." Verification differs per domain: a bash command, a test suite, a browser (Claude in Chrome), a phone simulator.

**Prompt engineering.** Two reusable prompts were shared:

- A **meta-prompt** ("You are an expert in prompt engineering. Given the following prompt, prepare it using best-practice structure — role, objective, etc. — and formatting…") that expands a one-liner such as "write unit tests for retrieving candidates for a position" into a full structured prompt with ROLE / CONTEXT / OBJECTIVE / SPECIFIC REQUIREMENTS / RESPONSE FORMAT / QUALITY STANDARDS sections, including explicit success, error and edge-case test lists.
- An **"ask the expert" prompt** for data modeling that ends with *"Analyze the project and ask me any questions you consider necessary to clarify before proposing the solution"* — i.e. force clarification before generation. (This matches Martin's existing preference for investigation-before-implementation prompts.)

### 3.3 Context engineering — "the perfect recipe"

Context is "the most important pillar". The recipe is a set of **separate files, each covering one element, all referenced from one base file**:

**Technical specifications**
- Tech stack.
- Development environment setup.
- Architecture and file structure.
- Data model entities (example rule file shown: `data-model.mdc`).
- Design patterns and conventions: API design patterns, test structure (`testing-standards.mdc`), naming rules, git workflow, clean code / SOLID, form-validation patterns, error handling, logging, security practices, how to document code and comments. Applies to backend, frontend and mobile (`frontend-standards.mdc`).

**Workflow** — write down, explicitly, the process from request to production:
- What happens, systematically?
- Who intervenes?
- What is each person's function and **deliverable** (PRD or user story, technical ticket, the code, tests proving the code matches the spec, a manual/automatic test report, documentation)?
- What makes each deliverable *excellent*?

Two structural rules: **one file per element, referenced from a base file**, and **one git worktree per ticket**.

The payoff the speaker describes: shared, updated context moves a team "from individual productivity to collective transformation" — consistency, coherence, **independence from the prompt** and **independence from seniority** (a junior with the right context produces senior-shaped output).

The Granola summary records the same idea in the speaker's words: context engineering is "giving the model memory, connectors and people-driven context" — tools, repos, Figma, Playwright, Confluence, external APIs — with the goal of *systematic, automated* improvement rather than ad-hoc manual effort. Functional documentation should be Confluence-style (readable by product people), not only technical docs.

### 3.4 Harness engineering

Opening metaphor: coding with agents without structure is "letting a robot loose in a kitchen without recipes". Harness engineering is the discipline that defines the instructions, tools, local environments and verification loops so the AI produces consistent, secure, production-ready code.

**The pyramid — three levels, each depending on the one below:**

1. **Context engineering (base)**: design what the agent sees before it answers — conventions, stack, workflow, hard constraints.
2. **Harness engineering (middle)**: build the whole environment the agent operates in — connected tools, automatic checks, access to your systems.
3. **Loop engineering (top)**: you no longer trigger the agent; you design the system that triggers it, checks results and decides what comes next. "The developer stops executing tasks and designs the system that executes them."

Higher = more leverage, but a loop built on disorganized context *amplifies* existing problems.

**The canonical formula** (attributed to Mitchell Hashimoto, HashiCorp co-founder): **Agent = Model + Harness.** The model supplies intelligence; the harness is everything else — the context it receives, the rules it respects, the tools it can reach, the tests/evals that verify output, the sandbox it runs in, the observability to know what it decided and why. Metaphor: *model = CPU, context = RAM, harness = operating system, agent = the application running on top.*

**"The model is almost never the problem"** — three cases cited:
- **Vercel** removed 80% of the tools from its text-to-SQL agent: success rate 80% → 100%, 3.5× faster, 37% fewer tokens. Same model, better harness.
- **LangChain** moved its coding agent from #30 to #5 on Terminal-Bench 2.0 (~14 points) without touching the model.
- **Stripe** merges ~1,300 PRs/week with no engineer writing the code — only reviewing.

**The five primitives of any harness** (attributed to Vivek Trivedy, LangChain), plus a sixth the speaker adds:
1. **Filesystem** — durable storage for state between steps.
2. **Code execution** — a terminal is a general-purpose computer.
3. **Sandbox** — isolated execution so the agent cannot break production.
4. **Memory & search** — continuous learning from project instructions, web search, vector knowledge bases.
5. **Context management** — compaction and offloading to fight *context rot* (quality decay as the context window fills with stale or irrelevant material).
6. **Guides and sensors** — *guides* act **before** execution (`AGENTS.md`, linters, constraints); *sensors* act **after** (tests, evals, validation). A good harness has both. *"Building the right sensors is one of the keys to a solid harness."*

**Frameworks for building your harness — and when to use each** (the speaker's honest comparison, including the weaknesses):

| Framework | What it is | Strength | Weakness | Use when |
|---|---|---|---|---|
| **OpenSpec** (Fission-AI) | Lightweight SDD based on **delta specs**: each change describes only what is ADDED/MODIFIED/REMOVED relative to the current spec. Flow: `/opsx:explore` → `/opsx:propose` → `/opsx:apply` → `/opsx:archive`. `npm i -g @fission-ai/openspec && openspec init`. ~60k GitHub stars, 30+ assistants supported. | Minimal friction; ideal for **brownfield** (existing) code; no rigid phases. | Multi-repo "Stores" feature is early beta with breaking changes. | You want to start today on a real project without infrastructure. |
| **Spec-Kit** (GitHub) | Most structured; explicit phases with checkpoints: `constitution → specify → clarify → plan → tasks → analyze → implement`. The *constitution* is the non-negotiable rules doc; `/analyze` checks spec/plan/tasks consistency before implementation. | Governance, auditability, compliance presets, 30+ integrations, GitHub/Microsoft backing. | Heavy for small tasks; sequential (no native parallel agents); CLI changed in v0.10 (older tutorials broken). Community opinions split. | Your organization needs everything documented and auditable. |
| **Superpowers** (obra / Jesse Vincent) | Not a spec framework — a library of **behavioral skills** installed as a plugin. Agent asks Socratic questions until a real spec emerges, builds a plan, then runs subagent-driven development with real TDD red/green/refactor, YAGNI, DRY as non-optional rules; native worktrees; auto-merge back. | Forced execution discipline; zero external dependencies; multi-agent-tool; maintainers reject 94% of PRs (rigor). | Produces no shareable spec document for team review. | What you lack is execution discipline (agent skipping tests), not planning. |
| **Spec-Boot** (LIDR) | Not a spec engine. A portable kit of rules, standards and agent configs: `docs/` with `api-spec.yml` (OpenAPI), `data-model.md`, `development_guide.md`, with symlinks so every copilot reads the same context. MIT, free. | Copilot-agnostic single set of rules. | Only the context layer; needs a spec engine on top. | Always — as the layer *under* any of the three above. (Note: LIDR's own product; weigh accordingly.) |

**Git worktrees** — explained at length because they are the mechanism that makes parallel agents safe:

A worktree is an additional working directory with its own folder and its own active branch, sharing history, objects and config with the main repo. Without worktrees, two agent sessions on the same directory overwrite each other, tests fail for unrelated reasons, the dev database ends up inconsistent. With one worktree per session, each agent sees only its own files and is unaware other sessions exist — *"the solution is not clever coordination between agents; it is physical isolation at the filesystem level, so they never need to coordinate."*

```bash
git worktree add ../my-project-payments feature/payments   # create
git worktree list                                          # list
git worktree remove ../my-project-payments                 # remove when done
claude --worktree feature-name                             # Claude Code native: creates, opens session, asks to keep/delete on exit
```

Claude Code also supports `isolation: worktree` for **subagents**, essential when splitting a large job across parallel subagents.

The **"worktree tax"**: each worktree is a fresh checkout (no `.env`, no `node_modules` — reinstall, or use a `.worktreeinclude` file to copy what is needed); shared databases or dev-server ports still collide (worktrees isolate files, not infrastructure — combine with per-branch DBs and per-session ports); for 10-minute tasks the setup may not pay off. Rule: *if you would normally create a branch to avoid conflicts, use a worktree; otherwise don't bother.*

### 3.5 Token savings

A well-built harness saves tokens. Badly used AI re-reads the whole repo every request, and every connected tool (skills, MCPs, terminal commands) adds tokens to every call. Five open-source tools, in order of installation ease (figures are each project's own claims):

1. **rtk** — compresses terminal output before the model sees it; 60–90% fewer tokens on common commands. github.com/rtk-ai/rtk
2. **codegraph** — a 100% local code graph the agent queries instead of exploring file by file; ~57% fewer tokens on average. github.com/colbymchenry/codegraph
3. **caveman** — strips filler from agent responses; ~65% fewer output tokens. github.com/JuliusBrussee/caveman
4. **ponytail** — targets the code the agent *writes*, not what it says; up to 80–94% less over-built code. github.com/DietrichGebert/ponytail
5. **Headroom** — compresses context (logs, tests) before it counts as input; up to 95% per its docs. github.com/headroomlabs-ai/headroom

The speaker reports ~60% personal savings ("my experience, not a lab benchmark"). Additional layers: automatic model **routing** ("Auto" modes in Cursor/Copilot; OpenRouter or LiteLLM at API level) and a trend toward **local models** (Qwen, Kimi, GLM) for well-defined tasks — re-verify the current versions before recommending to a team.

### 3.6 The verification debate (poll)

The closing poll exposed the central tension: *"If I have to hand-review everything the agent generates, I've only moved the bottleneck from writing code to reviewing code."* Versus: *"Trusting tests and evals 100% is reckless — a test passes even when the business logic is wrong."* The speaker's position: neither extreme; build the right **sensors** and keep a human on the decisions that matter. The Granola summary records the workshop's operational stance: **end-to-end tests (Playwright, Cypress) are mandatory, not optional**; the loop is *open spec → apply → verify → repeat*; PRs and git discipline are the baseline, with automatic review on commit/push and the team reviewing changes.

### 3.7 The live demo (from the Granola summary)

The demo implemented a **highlight-and-comment** feature as a worked example: domain-driven design, controllers in Ruby or JavaScript, endpoints GET/POST/DELETE around a comment/highlight model, with reports and highlights tied to each unit. An **open spec** was written as **user stories** (*"As a user, I want to sign up using SSO"*) and used as continuous context for the agent — the same format Martin was asked to reproduce.

### 3.8 Learning philosophy

Consuming tutorials is not learning; applying to real projects is. The speaker suggests an internal "professor/mentor" model for knowledge transfer inside teams, and "repo-based standards + an assistant" as practical scaffolding. On freelancing: viable, but competing requires champion-level skills.

### 3.9 The five embedded videos, digested

All five are on LIDR's YouTube channel except the last (a third-party Cursor tutorial). Verbatim transcripts live in `sources/raw/2026-09-08-lidr-workshop/`. Below, each is digested in English with every concrete practice preserved.

#### Video A — "¿Qué es un Agentic Engineer? El rol de software más demandado hoy" (5 min, 2026-07-15, `rdrtQyGhjYE`)

A clip from a live session. The speaker's metaphor: the agentic engineer goes **from artisan to manufacturer**. You no longer place every bolt; you supervise the assembly line that places it — you make sure the right machine is in the right place, and you know how to fix it when it breaks. Delegating programming to an agent is the same move: your job becomes orchestration.

Audience answers he read aloud (a useful vocabulary sample): "orchestrate agent tasks", "a dev who creates virtual devs", "supervision, orchestration, harnessing, guardrails", "managing workflows, monitoring the AI, creating and maintaining loops and harnesses".

His key distinction has two levels:

1. **The baseline (already a must in every job offer)**: an engineer who integrates AI effectively into daily work — knows Claude Code, knows some prompting, can operate a spec-driven setup someone else built. As a CTO running a job board he says companies have already changed their interview process to include LLM usage.
2. **The real agentic engineer (where the money is)**: the one who *designs the agentic layer* so that the whole team works the same, consistent way — "stops everyone fighting the war on their own". This is what companies hire LIDR for, because they lack the time or internal capability. It is "hyper-demanded" and paid better than a plain software engineer.

Long-term prediction: the role converges back into "software engineer", the way nobody says "VS Code engineer" or "Eclipse engineer". Controlling AI becomes as ordinary as knowing GitHub or Docker. "Harness engineering" is the name for this capability; he says the term had been in vogue for only about two months at recording time.

#### Video B — "Harness Engineering: Las 5 áreas clave para controlar y guiar a tus Agentes IA" (10 min, 2026-09-04, `fCkTax4WfRA`)

This is the most operational video and the one that defines LIDR's **five-area harness model**. The framing: a harness is "the leash, the limits we put on the agent about how to work". The kitchen analogy: a robot dropped into a kitchen with no recipes, no idea how to use a pan or an oven, no idea where the knives are, will not produce a dish.

The five areas, with the kitchen analogue and then the software artifact:

| # | Area | Kitchen analogue | Software artifacts |
|---|---|---|---|
| 1 | **Instructions** | The recipe book — how to make what is ordered | `CLAUDE.md` / `AGENTS.md` **plus all the technical context documentation that lives inside the code**. Where context cannot live in the repo, MCPs reach external sources (Confluence, Notion, Jira). |
| 2 | **Tools** | The knife — you must have it, and know how to use it | Command line, file access and manipulation, Git, MCP servers. |
| 3 | **Local environment** | The stove — where instructions and tools combine to actually cook | Clear dependencies and versions; which services can be launched; instructions to run tests, start the database, bring up the whole environment locally. *"If the agent can't run the code, can't start the DB, you can't give it an environment to work autonomously."* |
| 4 | **State** | The prep table (*mise en place*) — track where you are in the recipe, what you have used | A **persisted task artifact** that records where you left off — for when the session ends, the machine resets, another agent picks it up, or work is split across agents. |
| 5 | **Feedback** | The chef inspecting and tasting the dish before it goes out | Verification with the tools you already have: linter, build, unit tests, **end-to-end tests with Playwright or Cypress**, a Postman collection for API calls. If it passes → commit / PR; if not → correct. |

Two important additions the video makes to the hub text:

- **Feedback closes the loop on the harness itself.** Every failure feeds back into the harness: change the instructions, add tools, *remove tools that proved irrelevant*, fix the environment config. "A harness not only works with these five components; with that feedback it improves over time based on the developers' own usage."
- **The "before/after" demo.** Same code, now with a basic harness. The visible differences: a `docs/` folder holding backend standards, frontend standards, documentation standards, development guide, installation guide (the local-environment part), the data model, the full API model. His argument for why this matters: without it, the agent *explores whatever files it wants* to infer conventions, and two runs of the same task (or two developers) explore different files and produce different results. One consistent source of truth makes the AI "harder to distort". Documentation always used to rot because it lived somewhere else and nobody updated it; **if the AI updates it as part of every task and you only review the diff, the source of truth stays alive** — "that is the key: the context stays alive."

Layered on top of docs and `CLAUDE.md`/`AGENTS.md` he shows **skills** ("AI specs" in the captions) for anything repeatable: a `commit` skill that encodes how a commit is made; a code-audit skill run before finishing. Then **loops**: "when X happens (I ask for a commit / the agent finishes development), run the code audit first". He mentions a "run parallel tasks" loop that goes from a defined user story all the way to commit, but deliberately keeps the demo manual to show the fundamentals. The demo harness also has a few specialized agents and some scripts "for when I need something very deterministic". His closing line: this harness "is not perfect, not hyper-complete", but these are the ingredients — how to use the AI, which processes to follow, the technical context, the code conventions, how to bring up the environment.

#### Video C — "Spec-Driven Development: Cómo escalar tu productividad con IA y Contexto" (17 min, 2026-01-22, `eca3lWJgRmA`)

Despite the title, this video covers the first two pillars (tool and prompt) and explains *why they matter less now*: models have improved so prompt structure matters less, and once context is set up, daily prompts collapse to one-liners or slash commands. Prompts matter mostly **for generating the context in the first place**. Also: copilots have converged — Copilot, Cursor, Windsurf, Claude Code, Warp, Codex CLI all have roughly the same features; the demos use only features common to all.

**Copilot configuration.** "There isn't that much configuration, because what matters is how we provide context." The important settings are:

- **MCPs** (the most important). Three areas: *Context* — Jira (where user stories live) or Asana/Monday/Notion; Confluence/Notion for knowledge bases (information flows, use cases, full PRDs, product specs); **Context7** to feed the LLM the *exact version* of library/framework docs so it does not rely on training data (deprecated methods, current syntax); **Figma** so the LLM sees layers, texts, RGB colors, SVGs rather than an image, enabling pixel-perfect front/mobile work. *QA* — **Playwright**, which both generates automated QA test artifacts and can open a browser and navigate without a written test: "test the functionality n times at zero cost" while you do something else or are not at the computer. *Errors & security* — **Sentry** (errors) and **Snyk** (security): a prompt like "scan this directory for security flaws, vulnerabilities, dependencies" runs an analysis; the copilot can then implement the fixes **in a separate branch, in a separate worktree, as a background agent** while you work on the next feature. Goal: every task that reaches production includes an exhaustive error and security analysis.
- **Model**: at recording time he considered the choice "fairly irrelevant" given convergence; LIDR still recommends Claude models (Sonnet, Opus) as the most code-optimized, with Codex and Gemini Pro fully valid, and Cursor's own Composer as very fast. He leaves the model on **Auto** for cost; external models burn tokens faster; Composer gets more headroom. All editors have an auto mode, model choice, and some allow local models (Qwen).
- **Privacy mode** on (code not used for training) and **Memories** on (review/reset saved memories in settings).

**Two prompts that generate context.**

1. **Meta-prompt**: make the machine behave as the prompt-engineering expert; you state only the objective and expected result, it writes the prompt, and *that* prompt is what you run. Four lines you keep in a prompt library, or as a command. Example: "give me unit tests for get-candidates-for-position" (his ATS demo project) became a full prompt with role, technologies, project context, the specific function, current code, missing tests, mocking approach for the service/DB, parameter validation, AAA (Arrange-Act-Assert) methodology, and the explicit missing test cases.
2. **Ask-the-expert**: have a consultant on the other side who questions you before proposing. He wanted a data model for a new project; he gave the objective plus scattered clarifications, then: *"Analyze the project and ask me anything you need to clarify before proposing a solution."* Done in ChatGPT to show the model does not matter. It came back with three questions on auth, three on companies/seats, three on subscriptions and Stripe, three on report personalization and roles, three more on reports, four on chatting with reports, four on cross-cutting traceability/auditing, plus login, sensitive data, privacy, internationalization (storing texts in dedicated tables), and future scalability (indexes, normal forms). Answering exhaustively "is analysis work that helps us think better about the problem". Result: a full plan, table by table, with tips tied to his answers (e.g. "all sensitive data encrypted at rest" from the GDPR answer). Recommended 100% of the time for architecture and design tasks even if you are senior, and especially in areas where you are not the expert (data modeling from scratch, design/front-end for a backend dev). "When the rubber duck falls short, this is the pseudo rubber duck."

#### Video D — "Programa como un Senior con IA usando Context Engineering" (19 min, 2026-01-22, `okYRbetLh7M`)

The deepest of the five. Thesis: **context is the key regardless of whether you use spec-driven development.** The same task in another company would have different execution, validations and result; the AI must be *taught* the standards, not left to infer them per prompt from whatever files it happens to read. If you tell it where the testing, backend, frontend standards live, it goes to the same place every time → same information → consistent output.

**"Three ingredients and one golden rule."** Two ingredients are defined by the team — *technical specifications* and *workflow*; the third comes from outside — *the task* (endpoint, refactor, bug). With the machine prepared, only the task varies and the machine stays coherent across tasks. (The golden rule, stated at the end: **share the context with the whole team** so it becomes a team convention, not one person's productivity trick.)

**Ingredient 1 — Technical specifications**, in full:

- Stack: concrete technologies, versions, what each is for.
- Development environment: **fully** explained — from zero; how to start only backend+frontend when the DB is already running; how to seed the DB with concrete data (e.g. a pre-production sample); how to run unit tests; how to run integration tests.
- Architecture and file structure: hexagonal? DDD? where are repositories, services, routes, controllers?
- Data model entities: at least the main ones for a complex model, ideally with a diagram. **Each table documented in natural language**: what each field is for, main validation rules, which tables it relates to, then a **Mermaid diagram** at the end. Side benefit: non-technical people can read the Markdown, or hand it to ChatGPT, and stop interrupting the dev team.
- Design patterns and conventions: API design, test structure, naming rules, git workflow, patterns (factory, decorator…), clean code, SOLID, form validation (bad data, SQL injection), error handling, logging and code comments, security-by-design (XSS, CORS, SQL injection). Applies to frontend, backend, mobile and QA.

How he produces these documents — **prompts with a fixed index as a one-shot template**:
- README: *"Expert architect, prepare a README with at least these sections. Output in Markdown, properly formatted and indented, following this structure"* + the index. Giving the index "so it fills it in rather than inventing it" is the one-shot/few-shot technique. His README covers architecture, technologies, file structure, full setup instructions, how to test, a quick DB schema pointing to the full data-model doc, basic API docs linking to the full spec, and how to contribute.
- OpenAPI: *"You are an expert in API documentation with OpenAPI. This is the objective, this is the information it must contain, this format, this OpenAPI version, save it in this file/folder, follow these rules."* Gives frontend, external devs and even non-technical people exact visibility of the API.

**Ingredient 2 — Workflow (the SDLC blueprint).** Document, with a diagram, every phase from a new requirement to production and which role owns each phase. Teams "know it internally but rarely verbalize it". Verbalizing it helps the team and the business, but *especially the AI*, which then will not jump straight from ticket to code; it will know that the team applies **TDD (write tests, verify they all fail, only then implement after approval)**, that **updating technical documentation at the end is mandatory**, that **QA end-to-end tests with Playwright must pass**, that **the full unit suite must pass with a report showing nothing broke and new-feature coverage ≥ 90%**.

The **definition of done** must be written: what happens systematically, who intervenes, what each role's deliverable is. If the developer's deliverable is *code + updated documentation + unit tests*, the AI should deliver the same and **verify against a checklist before saying "done"**. If QA comes after, QA's output is *new tests + a report* handed to product. "This whole cycle has to be fully documented."

The standards documents themselves are **long — over 1,000 lines** for backend standards in a project smaller than most: technical overview, full stack, ORM usage, testing framework, dev tools (Postman), architecture diagram, applied DDD and SOLID principles, API standards, DB patterns, testing with examples, performance, security, git workflow (branch naming, where branches start, rebase or not, PR vs commit, merge to main or leave pending). "If we want the AI to think in systems and delegate parts of the process, we need a system." Same for frontend standards, documentation standards (how we write, when and where docs are updated, which code change triggers which doc update), and testing standards (unit-test rules, anti-patterns, integration with the rest of the workflow — run tests before every commit, all tests pass before merge, TDD, ≥90% coverage on new functionality). The AI helps write them: give it the index and tell it to be exhaustive and to act as the different experts per topic.

**Payoff.** This takes *days* — "a critical task for this year". Once done, share it: individual productivity → collective transformation. Consequences he lists: coherent code across your own attempts and across people; the agent reads `testing-standards` instead of inferring from test files (visible in its thinking); **independence from prompt quality** (prompts become "document this task", "plan by steps", "implement step 1", "give me unit tests"); **independence from seniority** — the same super-senior backend/testing/frontend agent answers junior and senior alike; add commands (`plan ticket`, `develop ticket`) and the output is the same for both. When evaluation shows tests/docs/code quality is good and the flow is respected, "you can hand the car keys to the junior", which is what multiplies team productivity.

#### Video E — "How to Use MCP Servers in Cursor" (4 min, 2025-05-23, `5s-lvoJpMTY`, third-party, English)

A mechanical walkthrough, included in the hub as the basic MCP example. Steps: find a server on a registry (glama.ai/mcp; the official filesystem server in the demo) → copy its JSON config (an `npx` command with arguments listing allowed folders) → install Node → Cursor settings → MCP tab → "add new global MCP server" opens `mcp.json` → paste into the `mcpServers` object → save → green dot (refresh if yellow) → in chat, *explicitly say "use the MCP"* because agents sometimes run terminal commands instead → approve each tool call. Dated (Claude 3.7 Sonnet, 2025 UI) but the mechanics are unchanged.

## 4. Claims worth checking

- All statistics in §3.1 and §3.4 are as cited by the speaker; none were re-verified for this entry. The METR and Faros figures are the most consequential — worth reading the originals before quoting them.
- Model recommendations (§3.2) are dated 2026-09-08 and will rot fast. The *principle* (top tier plans, mid tier executes) is more durable than the model names.
- The token-saving percentages are the tools' own marketing numbers.
- Terminal-Bench figures (Codex 77.3% vs Opus 65.4%) — verify version and date.

## 5. What is contested / trade-offs

- **Vendor interest**: LIDR sells the course and maintains Spec-Boot; OpenAI Academy defines "AI Champion". The framework comparison was notably even-handed (it lists Spec-Kit's critics), which raises trust, but Spec-Boot's "always use it" recommendation should be read as a pitch.
- **Spec-heavy vs. discipline-heavy**: the workshop itself flags that Spec-Kit can feel like bureaucracy for small tasks and Superpowers produces no reviewable spec. The right choice depends on team size and audit needs.
- **Verification**: the workshop leans toward automated sensors; other practitioners (see `sources/2026-09-08-how-teams-structure-agent-knowledge.md`) push the same direction but insist tests express *specs*, not just "it runs".
- **Worktrees**: real cost in setup and infrastructure isolation; not free.

## 6. Implications for Martin's repos

Martin runs several concurrent repos under `Local Coding/` (AI SDR, Content Central, WordPress Fleet Control, a report agent, Pagoralia, and others) and already works with Claude Code, Cursor, MCP servers and custom `CLAUDE.md` conventions. Mapping the workshop onto that:

- **Context files**: each repo should have the "recipe" set of separate files (stack, setup, architecture, data model, conventions, workflow with deliverables) referenced from a short base file. Today Martin's repos have `CLAUDE.md`/`AGENTS.md` conventions of varying depth — the audit playbook will reveal the gaps.
- **Spec-driven development**: OpenSpec is the lowest-friction fit for brownfield repos like AI SDR and Fleet Control. Spec-Kit is likely overkill for a solo operator. Superpowers could be layered later if agents keep skipping tests.
- **Worktrees**: Martin already has many `wt-*` folders in `Local Coding/` (e.g. `wt-copy-guards`, `wt-multiflow`) — he is using worktrees. The missing piece is probably `.worktreeinclude` and per-worktree DB/port isolation.
- **Verification sensors**: AI SDR (email pipeline, Postgres) and Fleet Control (WordPress automation) both need deterministic checks an agent can run — Playwright for WordPress UI, Hurl or pytest for APIs, and a Stop hook that runs them.
- **Token economy**: Martin hits weekly token limits on his plan; `rtk` (terminal output compression) and `codegraph` are the two cheapest wins to try first.
- **Model selection**: Opus in plan mode for specs and architecture; Sonnet for execution — matches his existing "Ciclo DIANA" lifecycle framing.

## 7. Actions

- [x] Create this knowledge base (`decisions/0001-knowledge-base-structure.md`).
- [ ] **Homework 1 (from the workshop)**: update every repo's technical context documents to match that project's specifics, following the structure in §3.3. → `playbooks/audit-repo-against-kb.md`, run per repo.
- [ ] **Homework 2 (from the workshop)**: draft an open spec for **single sign-on** as user stories, starting with *sign-up* and *login* flows. → `templates/open-spec-user-story.md`. Pick the repo (likely Pagoralia or AI SDR).
- [ ] Try `rtk` in one repo for a week; record token usage before/after in a new source entry.
- [ ] Evaluate OpenSpec on one small brownfield change in AI SDR; write up in `sources/`.
- [ ] Read the METR and Faros originals; annotate §4.

## 8. Raw notes (Granola auto-summary, verbatim structure)

*Harness Engineering and Context Engineering* — "harness engineering" as a distinct discipline encompassing prompt engineering, context engineering, loop design, latency control; sits above senior/architect level. Context engineering = memory, connectors, people-driven context (tools, repos, Figma, Playwright, Confluence, external APIs); goal systematic/automated improvement. Role distinction harness engineer vs product engineer vs senior implementer; harness engineer owns the full interaction layer; requires end-to-end architecture understanding.

*Development Standards and Testing* — E2E testing (Playwright, Cypress) mandatory; TDD loop: open spec, apply, verify, repeat; reports and highlights tied to each unit; PRs and git control as baseline; automatic revision on commit/push; highlight/commentary system as implementation example (Ruby or JS controllers, DDD, GET/POST/DELETE around a comment model); open spec format as continuous context; SSO spec as user stories; functional documentation Confluence-style.

*Skills, Roles, Learning Path* — ~15–20% reach strong senior level, fewer champion/lead; champion = global approach, system-resistance awareness, strategic mindset; harness engineer profile (full-stack, testing/accessibility/scalability, AI/ML layer: LangChain, LangGraph, AutoML, Microsoft agents, orchestration); tutorials ≠ learning; internal mentor model; repo-based standards + assistant as scaffolding; freelance viable at champion level.

*Next steps* — update all technical context documents to match project specifics, following the existing docs structure; draft open spec for SSO as user stories, sign-up and login first.
