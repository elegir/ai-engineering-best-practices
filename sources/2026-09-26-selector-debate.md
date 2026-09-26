---
title: "Selector debate — proposal v1, the devil's-advocate attack, the responses, and the agreed design v2 (applicability by facts)"
type: source
status: current
date: 2026-09-26
tags: [debate, applicability, selector, decision-record, devils-advocate]
sources:
  - sources/2026-09-26-selector-research.md
  - decisions/0003-applicability-by-facts.md
supersedes: null
superseded-by: null
---

# Selector debate (2026-09-26)

Method: a design proposal was written from the research, then a separate agent that had not seen the proposal being written attacked it (18 attacks, each with a concrete example from this repo or from Martin's real projects), then the author answered each attack — concede, defend, or partly — and the surviving design became `decisions/0003-applicability-by-facts.md`. All three artefacts are kept verbatim below so the reasoning can be audited. This debate format is now part of the protocol for any structural change to the KB (see `playbooks/ingest-new-source.md`, "Structural changes").

---

# Part 1 — Proposal v1 (as attacked)


Author: Claude (for Martin). Date: 2026-09-26. Status: draft for adversarial review. Research basis: `/home/claude/research/selector-research.md`.

## Goal

Any software project — at day one or later — points a coding agent at this KB, answers a short profile, and gets back **only the practices that apply to it**, ranked by risk, with each one either applied through the existing `practices/<name>/` folder or explicitly marked "does not apply, because …". The KB must stay small and current while the number of practices grows (17 course modules will add ~14 practice folders to the current 10).

## Design (what I propose to build)

### D1. One core, many lenses — but the lens *is* the practice's applicability rule, not a separate document
AWS/Google/Azure separate a universal core (pillars) from overlays (lenses). We do not need separate lens documents: our `practices/` folders already carry an "Applies when / Does not apply when" section in prose. We add a **machine-readable form of that section** to each practice's frontmatter and keep the prose. The "core" is simply the set of practices whose rule is `always`. Rule: the core may hold at most 6 practices; `kb-check.sh` fails otherwise.

### D2. The project profile: ≤12 enum dimensions in one file in the target repo
`docs/project-profile.yml` in the *target* repo (pointer from its `CLAUDE.md`/`AGENTS.md`), answered once, re-answered when it changes:

```yaml
schema: 1
stage: greenfield | brownfield
traffic: none | internal | production
team: solo | small | multi-team
tenancy: single | multi
data: none | personal | regulated
regions: [mx, us, eu]
ui: none | api | web | chat
llm: none | calls | rag | agent-tools | multi-agent      # cumulative ladder
autonomy: 0 | 1 | 2 | 3                                  # 0 no side effects … 3 unsupervised irreversible actions
stack: {lang, runtime, hosting}                          # selects variants only, never applicability
rigor: {security: 1|2|3, reliability: 1|2|3, agent-safety: 1|2|3}   # per-topic target; default 1
exemptions: [{practice, reason}]                         # technical reason required
```

Every dimension must be referenced by at least one practice's rule, or it is deleted (Google's checklist rule). `stack` picks which variant file to copy; it never decides whether a practice applies.

### D3. Practices declare applicability as a tiny boolean expression, plus strength and minimum rigor
Three new frontmatter fields on every `practices/*/README.md`:

```yaml
applies-when: "llm in [agent-tools, multi-agent] and traffic == production"   # or: always
strength: default | recommended | consider     # default = on unless exempted (Thoughtworks "sensible default")
rigor-min: {agent-safety: 2}                    # optional; attach only when the profile's target rigor is ≥
```

Grammar: `==`, `!=`, `in [..]`, `and`, `or`, `not`, parentheses, over profile enums. Small enough for a human to read, for an agent to reason over, and for a ~40-line `scripts/select-practices.py` to evaluate deterministically. Tags are rejected because they cannot express AND/NOT ("multi-tenant AND production").

### D4. The selector loop, run by the agent in the target repo (playbooks/profile-a-repo.md (rejected, not built))
1. Read `docs/project-profile.yml`; if missing, ask the ≤12 questions (each with its enum and one sentence on why it matters), write the file, **stop for approval**.
2. Evaluate every practice's `applies-when` → four states: `applies (default)`, `applies (consider)`, `skipped (rule false — reason auto-generated from the prose "Does not apply when")`, `exempt (reason from profile)`.
3. Rank applicable-but-absent practices by risk: `default` × (`traffic == production` or `data != none`) = HIGH; `recommended` = MEDIUM; `consider` = LOW. Present the plan; stop for approval.
4. Apply through the practice folders (copy, replace placeholders, run Verify); prefer generated hooks/tests over prose.
5. Record in the target repo's harness changelog: profile hash + the four-state table, so a later audit diffs against it.
6. A path-scoped rule `.claude/rules/profile.md` (`paths: ["docs/project-profile.yml"]`) reminds the agent to re-run the selector whenever the profile file is touched.

`playbooks/audit-repo-against-kb.md` calls this playbook first; the existing audit then only inspects the practices that apply.

### D5. Guardrails against the known failure modes, enforced by `kb-check.sh`
- Core ≤ 6 practices; every practice has `applies-when`; every expression references only declared dimensions; every dimension is referenced.
- Three fixture profiles in templates/profiles/ (rejected, not built) (solo greenfield API with one LLM call; multi-tenant production SaaS with agents; EU chat product with RAG) are run through the selector on every check; fail if fixture 1 selects more than 8 practices.
- Any practice with `last-reviewed` older than 12 months is flagged "review before applying" in the selector output.
- "Not applicable" is a first-class state with a reason (ASVS/GitLab), never silence.

### D6. Where it lands in the repo
- principles/10-applicability-and-project-profiles.md (rejected, not built) (draft): the why.
- templates/project-profile.yml (rejected, not built), templates/profiles/*.yml (rejected, not built) (fixtures).
- playbooks/profile-a-repo.md (rejected, not built); `audit-repo-against-kb.md` amended to call it.
- Frontmatter fields on the 10 existing practices, derived from their prose; `practices/_template/README.md` updated.
- `scripts/select-practices.py`; checks added to `scripts/kb-check.sh`.
- `AGENTS.md`: new job "Profile" and the one-line rule for other repos.

## What I am deliberately not doing
- No scores or weights; enums only (false precision).
- No separate lens documents (two taxonomies).
- No automatic inference of the profile from the code in v1 (metadata rot is real, but inference is a v2 problem: the audit playbook can flag contradictions such as a `tenant_id` column with `tenancy: single`).
- No rigor levels outside security / reliability / agent-safety.


---

# Part 2 — The devil's advocate

Date: 2026-09-26. Reviewer: Claude (adversarial pass, requested by Martin's session). Inputs: `(below)`, ``sources/2026-09-26-selector-research.md``, and the repo at `(below)` (`AGENTS.md`, `INDEX.md`, `practices/README.md`, all ten `practices/*/README.md` "Applies when" sections, `playbooks/audit-repo-against-kb.md`, `scripts/kb-check.sh`, `decisions/0001-knowledge-base-structure.md`, `principles/09-knowledge-base-design.md`, `skills/apply-ai-engineering-kb/SKILL.md`).

Severity scale: **fatal** (the proposal as written cannot ship or cannot work), **serious** (ships, then fails or is ignored within weeks), **minor** (fixable in an hour).

---

## 1. Nine of the ten existing practices are `always`, so the "core ≤ 6" rule fails on day one — and `kb-check.sh` going red blocks every publish

**Claim under attack.** D1: "The 'core' is simply the set of practices whose rule is `always`. Rule: the core may hold at most 6 practices; `kb-check.sh` fails otherwise." D5: "every practice has `applies-when`; … every dimension is referenced."

**Why it fails.** I tried to write the rule for each existing practice from its own prose:

| Practice | Its prose "Applies when" | Honest `applies-when` |
|---|---|---|
| `verification/` | "Any repo where an agent changes behavior. … Does not apply when: Nothing." | `always` |
| `agent-entry-file/` | "Any repo an agent works in more than once. … Does not apply when: Nothing." | `always` |
| `prompt-library/` | "Any repo. … Does not apply when: Never fully." | `always` |
| `context-docs-skeleton/` | "more than a weekend of work … touched by an agent more than once" | `always` (no dimension says "weekend") |
| `session-state/` | "Any task longer than one session" | `always` |
| `spec-driven/` | "Any change bigger than one file" | `always` (a per-change test, see #7) |
| `token-savings/` | "Any repo where you hit limits" | `always` (depends on Martin's plan, not the project) |
| `hooks-and-guards/` | "repo has a formatter/linter and a test command; Claude Code is one of the agents" | `always` (both conditions are tooling facts, not profile dimensions) |
| `worktrees/` | "More than one agent session … at the same time" | no dimension expresses this (see #6) |
| `agent-patterns/` | "A feature lets a model decide what to do next" | `llm in [agent-tools, multi-agent]` — the only real one |

Nine `always`, one conditional. The proposal's own check fails immediately, and `playbooks/publish-change.md` + `CLAUDE.md` ("Do not run `git commit` on `main` directly", `/publish` runs `kb-check.sh` first) means a red check stops *all* KB work, including unrelated course ingestion, until someone either (a) invents conditions the prose does not support, or (b) raises the cap to 10, at which point the "core" is the whole KB and the selector selects nothing.

**Concrete example.** The proposal says the fields are "derived from their prose". Derive `context-docs-skeleton/`: the prose is about repo age and how many agents touch it; nothing in `stage/traffic/team/tenancy/data/regions/ui/llm/autonomy` encodes "more than a weekend of work". The only way to make it conditional is to lie (`stage == brownfield`), which then wrongly skips it for every new project — the exact day-one case the KB is for.

**Severity: fatal.**

## 2. The schema's own deletion rule collapses it to two questions

**Claim under attack.** D2: "Every dimension must be referenced by at least one practice's rule, or it is deleted (Google's checklist rule)."

**Why it fails.** Apply the rule to the 10 current practices plus the ~14 planned ones (LLM API wrapper, prompt caching, structured outputs, guardrails, memory, evals, data ingestion, chunking/embeddings, vector store, RAG pipeline, agent patterns, multi-agent/security, LLMOps, spec-driven/skills/MCP). Every one of the 14 is gated by *one* thing: where the project sits on the `llm` ladder (none / calls / rag / agent-tools / multi-agent), occasionally `autonomy`. Nothing planned reads `stage`, `team`, `tenancy`, `regions`, `ui`. `traffic` and `data` appear only in the risk formula (D4 step 3), not in any `applies-when`. By the proposal's own rule those seven dimensions are deleted, and the profile is `llm` + `autonomy`. That is a two-line "which rung of the ladder are you on?" question, which the agent can ask in one sentence without a schema, a grammar, a Python evaluator, three fixtures, or a new principle.

**Concrete example.** `regions: [mx, us, eu]` — "EU triggers GDPR-related practices". There is no GDPR practice in the KB and none in the 17 modules. Dead on arrival.

**Severity: serious** (the structure survives, but 80 % of it is inert weight; combined with #1 it means the machinery exists to distinguish `agent-patterns` from everything else).

## 3. Martin will answer the questions wrong, and the schema cannot tell

**Claim under attack.** D2, D4 step 1: "answered once … ask the ≤12 questions (each with its enum and one sentence on why it matters)".

**Why it fails.** The enums look crisp but the projects do not fit them. Two real profiles:

*Cold-email SaaS for US law firms (AI SDR, multi-tenant).*
- `traffic`: "real users hitting it?" — no human users hit it; it hits 5,000 lawyers a week. Martin will say `internal`. Every `traffic == production` rule then misses the one system that can burn his sending domains and get him sued.
- `data`: lawyers' names, firm emails, reply text — CAN-SPAM/GDPR-relevant PII. Martin will say `none` ("it's just business contacts"). The proposal's risk formula (`data != none`) then rates a system that stores thousands of third-party contact records as low risk.
- `autonomy`: it sends emails with no human review — irreversible side effects on strangers. That is `3` by the proposal's own scale ("unsupervised irreversible actions"). Martin will say `1` because in his head "it just sends emails". The `agent-safety` practices from the multi-agent/security module never attach.
- `llm`: the ladder is "cumulative", so `agent-tools` implies `rag`. AI SDR has tool use (research, send) and no RAG. Any rule written `llm == rag` (the RAG pipeline, chunking, vector-store practices) fires wrongly on it, and any `llm in [rag, agent-tools]` written to mean "has retrieval" fires too.

*RSS-to-WordPress pipeline (Content Central).*
- `llm`: rewrites articles (`calls`) and publishes through the WordPress REST API (a tool). Is that `agent-tools`? By `practices/agent-patterns/README.md` "Does not apply when: The feature is one LLM call with a fixed prompt", it is `calls`. But the pipeline *does* take irreversible actions (publishes to public sites). The ladder conflates "how smart is the model's control flow" with "does it act on the world", so `autonomy: 3` with `llm: calls` is a legal but unforeseen combination no rule will be written for.
- `tenancy`: one owner, 40 sites, per-site config — `multi` or `single`? Both defensible. The SaaS-lens meaning (many *customers*) is not what Martin will hear.
- `ui: none` — it has a WordPress admin. Martin will say `web`.

None of these wrong answers produce an error; they produce a confident, wrong plan with "HIGH/MEDIUM/LOW" labels on it. The research itself warned about this (§4.4 "False precision") and the proposal's only mitigation, "coarse enums", is what causes it.

**Severity: fatal** for the "correct selection" goal; the selector is only as good as twelve answers a vibe coder gives by voice on a phone.

## 4. The `llm` "cumulative ladder" is not cumulative

**Claim under attack.** D2: `llm: none | calls | rag | agent-tools | multi-agent      # cumulative ladder`.

**Why it fails.** A ladder means each rung includes the ones below. RAG is not a prerequisite for tool use (AI SDR: tools, no RAG); multi-agent systems frequently have no RAG; a chat product can have RAG and zero tools. So `llm` is at least two independent booleans (`retrieval`, `tools`) plus a multi-agent flag, and the proposal's grammar has no way to say "has retrieval regardless of rung". Every future RAG-module practice (data ingestion, chunking, vector store, RAG pipeline — four of the fourteen) will be mis-gated.

**Concrete example.** `applies-when: "llm == rag"` on `rag-pipeline/` → skipped for a multi-agent product that has RAG. `applies-when: "llm in [rag, agent-tools, multi-agent]"` → applied to AI SDR, which has no retrieval, producing a "HIGH: missing vector store" finding.

**Severity: serious.**

## 5. The grammar cannot address half of the profile it is defined over

**Claim under attack.** D3: "Grammar: `==`, `!=`, `in [..]`, `and`, `or`, `not`, parentheses, over profile enums."

**Why it fails.** Three of the twelve dimensions are not enums: `regions` is a list, `stack` and `rigor` are maps, `exemptions` is a list of objects. `in [..]` is scalar-in-list; there is no "list contains" (`eu in regions`), no map access (`rigor.security >= 2`), no ordering (`autonomy >= 2` — the one comparison the CSA-tier idea needs). So the rules that were the *motivation* for a grammar over tags ("multi-tenant AND production", "autonomy tier drives obligations") are writable only for `tenancy`/`traffic`; the autonomy ladder must be spelled `autonomy in [2, 3]`, which silently breaks when a `4` is added. `rigor-min` is bolted on as a separate field precisely because the grammar cannot express it, which is the first sign the grammar is too small for its own schema.

Also: "a ~40-line `scripts/select-practices.py`" — a correct recursive-descent parser with precedence for `not`/`and`/`or`, parentheses, `in` with list literals, plus YAML frontmatter extraction (PyYAML is not in the standard library; `scan-filter.py` is the only Python in the repo and `CLAUDE.md` says "do not create build tooling") is not 40 lines. The realistic alternative, `eval()` after string munging, is the thing every security practice in the planned modules will tell agents not to do.

**Severity: serious.**

## 6. `worktrees/` — the practice Martin actually uses — has no dimension

**Claim under attack.** D6: "Frontmatter fields on the 10 existing practices, derived from their prose."

**Why it fails.** `practices/worktrees/README.md` applies when "More than one agent session (or a session plus Martin) works on the same repo at the same time." That is a fact about *how Martin works this week*, not about the project. The nearest dimension is `team`, and Martin's answer is always `solo` — yet solo-with-three-Claude-sessions is exactly the worktree case (`principles/06-parallel-agents-and-worktrees.md`). Writing `team != solo` skips the practice for its main user; writing `always` contradicts the prose "Does not apply when: ten-minute fixes done one at a time." The research's own example exemption for worktrees ("single developer, single branch at a time", §4.1) is, by the ASVS rule the same document quotes ("lack of implementation time cannot" justify N/A), not a technical reason — it is a workflow preference. The proposal's flagship example breaks its own N/A rule.

**Severity: serious.** The fix (a `parallel-sessions: yes|no` dimension) is a workflow question, which the schema explicitly excludes ("project profile").

## 7. Spec-driven development is a working style, not a project property; the selector adds nothing and hides the one real branch

**Claim under attack.** Implicit in D1/D3 that every practice, including `spec-driven/`, gets a meaningful `applies-when`.

**Why it fails.** `practices/spec-driven/README.md`: "Applies when: any change bigger than one file or touching behavior users see. Does not apply when: typo fixes, dependency bumps." That is a *per-change* test (evaluated by the agent at `/plan-ticket` time), not a per-repo test. Per repo the answer is `always`, so the selector's contribution to the practice Martin cares most about is a row that says "applies (default)". The one genuinely conditional line in that README — "Brownfield repos (most): use the manual flow first, then OpenSpec's delta specs" — is a *variant* choice driven by `stage`, and D2 says variants are chosen by `stack` only ("`stack` picks which variant file to copy; it never decides whether a practice applies"). So the schema has `stage` but forbids using it for the only thing `stage` is good for.

**Severity: serious** — for the practice Martin named as his priority, the machinery produces zero information and blocks the useful one.

## 8. The risk ranking is theatre for Martin's portfolio

**Claim under attack.** D4 step 3: "`default` × (`traffic == production` or `data != none`) = HIGH; `recommended` = MEDIUM; `consider` = LOW."

**Why it fails.** Every product Martin has is live (AI SDR, Content Central, WP Fleet, real-estate site, fintech). If answered honestly they are all `production` and all `data != none` (contact lists, WP credentials, tenant configs, payment data). So every absent `default` practice is HIGH on every repo — the ranking never discriminates *between* practices, which is what a ranking is for. Conversely, fixture 1 (traffic none) rates a missing `verification/` — the practice the KB itself says to install *first* — as MEDIUM. `practices/README.md` already has a better ordering ("Recommended order for a repo with nothing: verification → context-docs-skeleton → agent-entry-file …") and `audit-repo-against-kb.md` §Step 4 already encodes it as a nine-step priority. The proposal replaces a considered order with a two-bit formula that yields "everything HIGH".

**Severity: serious.**

## 9. `rigor` defaults to 1, so the security practices for the fintech and the multi-tenant SaaS silently never attach

**Claim under attack.** D2 `rigor: … default 1`; D3 `rigor-min: {agent-safety: 2}  # attach only when the profile's target rigor is ≥`; research §4.4 "rigor defaults to 1 and must be raised deliberately with a reason".

**Why it fails.** The practices that will carry `rigor-min ≥ 2` are precisely guardrails, tenant isolation, agent sandboxing, LLMOps monitoring — the multi-agent/security and guardrails modules. A solo vibe coder who has never heard of ASVS will never "deliberately raise rigor with a reason"; the default is what ships. Result: the fintech (`data: regulated`) and the multi-tenant SaaS run at `security: 1` forever and the selector *certifies* that the L2 practices "do not apply". This is the ASVS misuse the research quotes ("L2 because it is the middle number") inverted into "L1 because it is the default", with a written record making it look intentional.

**Concrete example.** Profile `tenancy: multi, traffic: production, data: personal, rigor: {security: 1}` → `tenant-isolation/` (`rigor-min: {security: 2}`) → state `skipped`. The four-state table says "skipped (rule false — reason auto-generated)". The auto-generated reason will be nonsense, because the prose "Does not apply when" of a tenant-isolation practice will not say "when the owner didn't raise rigor".

**Severity: fatal** for the stated purpose ("ranked by risk"); it is the mechanism most likely to produce a confidently wrong "N/A".

## 10. "Skipped, reason auto-generated from the prose" is not the ASVS technical reason the proposal claims

**Claim under attack.** D4 step 2: "`skipped (rule false — reason auto-generated from the prose 'Does not apply when')`"; D5: "'Not applicable' is a first-class state with a reason (ASVS/GitLab), never silence."

**Why it fails.** ASVS's rule (research §1.3) is that N/A needs a technical explanation *about this system* ("absence of password recovery can justify excluding recovery-specific controls"). Pasting the generic "Does not apply when" bullet is a template, not evidence. `worktrees/` skipped → "Ten-minute fixes done one at a time in the main checkout" pasted into the AI SDR audit, a repo where Martin runs parallel sessions. GitLab's `skipped` state (research §1.6) is meaningful because a human declared the exclusion per service; here it is a boolean's side effect. The existing `audit-repo-against-kb.md` §Step 3 already requires the stronger thing: "whether its 'Applies when' holds for this repo (quote the condition)" — evaluated by the agent reading the repo. The proposal downgrades that.

**Severity: serious.**

## 11. The fixture check "fixture 1 ≤ 8 practices" is arbitrary today and gameable tomorrow

**Claim under attack.** D5: "fail if fixture 1 selects more than 8 practices."

**Why it fails.** (a) Today: with nine `always` practices (#1), fixture 1 selects ≥ 9 and the check is red before a single fixture is written. (b) Tomorrow: the cheapest way to make it green is to flip a practice from `default` to `consider` or to add `and traffic == production` to its rule — neither changes the KB's advice, both change the count. The check measures the size of the `always` set, which is already checked by "core ≤ 6", so it is redundant with a different number. (c) The number 8 has no source; the research says "~8" as an example and the proposal promoted it to a gate. Google's LCE rule was "substantiated by a previous launch disaster" — the proposal has no disaster to point to.

**Severity: minor** in isolation, **serious** combined with #1 because two red checks block publishing.

## 12. Adding a dimension or a practice has no maintenance story, and the profile in every target repo has no migration story

**Claim under attack.** D5 and D6 generally; D2 `schema: 1`.

**Why it fails.** Two directions, both unhandled:

- *New dimension* (e.g. a course module needs `retrieval: none|static|agentic`). Every existing rule ignores it; `kb-check.sh` cannot tell "intentionally ignores" from "forgot". The `schema` number in every target repo's `docs/project-profile.yml` is now stale; nothing re-asks the question. The proposal names metadata rot (research §4.4) and defers inference to "v2" — but the rot starts the day the second dimension changes, which is the day the second course module lands.
- *Deleted dimension* (the "delete unreferenced dimensions" rule). Target profiles now carry keys the selector does not know; the script either errors or silently drops them.
- *New practice from a course module.* `playbooks/ingest-new-source.md` (the one protocol for new material, per `AGENTS.md`) has no step "write `applies-when`, `strength`, `rigor-min`, re-run fixtures". The impact table has no column for it. So each new practice is created by an agent that has not read the grammar, and `kb-check.sh` rejects it → the ingest branch cannot publish → the agent "fixes" it by writing `always` → #1 again.

Twenty-four practices × three fields × twelve dimensions, curated by one person who does not write code, with no owner for consistency. Cortex/OpsLevel (the research's models) have a product team for this.

**Severity: serious.**

## 13. The profile file and the path-scoped rule violate decision 0001 and Martin's stated boundary

**Claim under attack.** D2 "`docs/project-profile.yml` in the *target* repo"; D4 step 6 "A path-scoped rule `.claude/rules/profile.md`"; D4 step 1 "write the file, **stop for approval**".

**Why it fails.** `decisions/0001-knowledge-base-structure.md` (status `accepted`, which `AGENTS.md` says to respect): "Other repos consult it by a prose pointer … They do **not** copy files from it." The proposal has the KB dictate two new files in every target repo, one of them a Claude Code rule that fires on every touch of the profile. `playbooks/audit-repo-against-kb.md`: "**No other files are changed by this playbook.** Implementation happens only after Martin approves." D4 step 1 writes the profile *before* the approval stop. And Martin's own stated boundary (project notes): "deciding what to adopt is the job of the agent in each target repo — Martin does not want audits or changes to other repos driven from the KB work itself." A KB-defined schema file whose hash is recorded in the target's changelog and whose edits re-trigger the selector is the KB driving the target repo.

**Severity: serious** (it needs a new decision superseding 0001, which the proposal does not propose).

## 14. Token cost: the agent must open every practice README to evaluate rules and quote reasons; INDEX.md is the natural home and is ignored

**Claim under attack.** D4 step 2 "Evaluate every practice's `applies-when`"; D4 step 2 "reason auto-generated from the prose".

**Why it fails.** Frontmatter can be grepped cheaply, but the "reason from prose" requires the body, so the honest evaluation reads all ~25 READMEs (currently 673 lines for 10; ~1,700 lines at 25) on every profile run, before any repo file is read. The research's own §1.9 says every mechanism that works imposes a size budget ("~100-token metadata, load-on-demand"). The repo already has the compact table the research describes: `INDEX.md` "Practices" table and `practices/README.md` "The practices" table (name / solves / principle / difficulty). One extra column "Applies when (one line)" in that table is the whole progressive-disclosure design, costs ~25 lines, and the agent already reads `INDEX.md` first per `AGENTS.md` and `SKILL.md`. The proposal instead scatters the signal across 25 frontmatters and adds a script to gather it back.

**Severity: minor** in tokens, **serious** as a design smell: the machine-readable form is put where the agent does not look.

## 15. The proposal ignores the research's strongest finding: templates and inheritance beat checklists

**Claim under attack.** The whole design is questionnaire → rule → checklist of practices.

**Why it fails.** The research (§1.2, §1.6, §3.7) is explicit that Google's fix for PRR overhead was frameworks ("a service inherits the standards by construction"), Spotify's is Golden Paths (one path per software type; "practices are inherited rather than checked"), and Anthropic's is that prose is "context, not enforced configuration". For a solo owner with five known project shapes (multi-tenant SaaS with an agent; scheduled publishing pipeline; WordPress tooling; marketing site; fintech), the direct translation is three to four *golden-path bundles* — "new LLM-calls pipeline on Digital Ocean", "new multi-tenant agent SaaS", "new content site" — each a ready-to-copy set of files. Martin would answer one question ("which of these is it closest to?") instead of twelve, and the bundle is testable in the KB (`kb-check.sh` can smoke-test a bundle; it cannot smoke-test a boolean rule). The proposal's "Deliberately not doing" list does not mention golden paths, so the option was not considered, not rejected.

**Severity: serious** (it is the better first thing to build; see #18).

## 16. It doubles the mechanism the coding agent already has

**Claim under attack.** D3 "for an agent to reason over, and for a ~40-line script to evaluate deterministically."

**Why it fails.** What does determinism buy here? The selector's output goes to the same agent that then reads the repo, judges variants, writes reasons and stops for approval — every downstream step is judgment. Two evaluators of the same rule (script and model) can disagree, and when they do, the proposal does not say who wins. The research (§1.9) shows what actually loads context conditionally today: a Skill `description` matched by the model, a `.claude/rules` `paths` glob. A one-paragraph "Who this is for / who should skip it" in each README, plus the table column from #14, is read by the model in one pass and can express things no enum can ("you run more than one Claude session on this repo", "you have already been bitten by a red suite marked done"). The deterministic script only earns its keep if something *mechanical* consumes its output (CI failing on a missing practice), and nothing in the proposal does — D4 step 4 explicitly hands back to the agent.

**Severity: serious.**

## 17. The interaction model contradicts how Martin works

**Claim under attack.** D4 step 1: ask "≤12 questions (each with its enum and one sentence on why it matters)"; research §4.4 "answerable in ten minutes".

**Why it fails.** Martin dictates by voice on mobile, in Spanish, and has asked for "one action at a time and confirmation before proceeding". Twelve enum questions with nested maps (`rigor: {security, reliability, agent-safety}` is three more) and a why-sentence each is 15 round trips per repo × 5 repos, answering things like "autonomy tier 0–3" and "regulated vs personal" that require definitions he does not have. He will say "you decide", the agent will fill the YAML, and the "profile hash" recorded in the changelog will certify answers nobody gave. Compare `audit-repo-against-kb.md` §Step 1, which already infers the same facts read-only from the repo and never asks.

**Severity: serious.**

## 18. Wrong first thing to build

**Claim under attack.** D6 — nine new artifacts (principle, template, fixtures, playbook, script, check changes, frontmatter on 10 practices, `AGENTS.md` job, audit-playbook amendment) before a single practice has been applied through the KB to a real repo.

**Why it fails.** `INDEX.md` "Open actions" still lists "Workshop homework 1: … run `audit-repo-against-kb.md` per repo" as unchecked. The audit playbook — the existing selector — has not been run once. Building a second selector before the first has produced one finding is optimising a loop with zero iterations. The cheap version that gets the same benefit this week: (1) one column "Applies when (one line) / Skip when" in `practices/README.md`'s table; (2) a one-page `playbooks/which-practices-apply.md` decision guide with Martin's four project shapes as worked examples; (3) run the audit on AI SDR and see which "Applies when" prose was actually ambiguous. The proposal's own research says catalogues survive by aggressive pruning and "substantiated by a previous launch disaster"; the KB has no disaster yet to substantiate a schema.

**Severity: serious.**

---

## The three most likely to kill it in practice

1. **#1 + #11 — the guardrails go red on day one and block publishing.** Nine of ten practices are honestly `always`; "core ≤ 6" and "fixture 1 ≤ 8" fail before any fixture exists; `/publish` refuses; the only exits are fake conditions or a raised cap that makes the core the whole KB. This is not a tuning problem, it is the design measuring the wrong thing: this KB is mostly universal working-style practices, and the conditional part is one ladder (`llm`) plus `autonomy` (#2).

2. **#3 + #9 — the profile will be answered wrong and the selector will certify the wrong answer.** The cold-email SaaS gets `traffic: internal, data: none, autonomy: 1, rigor: 1` from a solo owner answering by voice; the security/agent-safety practices for a multi-tenant system that emails thousands of strangers unsupervised are marked "skipped" with a pasted boilerplate reason and a HIGH/MEDIUM/LOW label that never varies across his repos (#8). A wrong plan with a hash in the changelog is worse than no plan.

3. **#13 + #15 + #18 — it builds the wrong thing against a standing decision.** The design pushes KB-defined files and a re-trigger rule into every target repo, against `decisions/0001-knowledge-base-structure.md` and Martin's stated "the KB does not drive changes in other repos", while ignoring the research's own strongest pattern (golden-path bundles per project shape, one question instead of twelve) and skipping the cheap version (a one-line "applies when" column in `practices/README.md` plus a one-page decision guide) that would show within a week whether any of this machinery is needed.


---

# Part 3 — Responses and agreed design v2

Date: 2026-09-26. Format: attack → response (concede / defend / partly) → resolution. Inputs: (below), (below), `sources/2026-09-26-selector-research.md`.

## Round 1 — the attacks that stand

**#1 Nine of ten practices are `always`; "core ≤ 6" goes red on day one.** *Concede.* The attack found the real structure of this KB: it is mostly **working-style** practices (how an agent works in any repo) plus a growing set of **capability** practices (what the product does). A cap on the core measured the wrong thing. Resolution: make the two kinds explicit; no cap; the "core" *is* the working style.

**#2 The deletion rule collapses the schema to `llm` + `autonomy`.** *Concede, and it is good news.* The conditional part of the KB is small and concrete. Resolution: replace twelve enum dimensions with ~10 observable **facts**.

**#3 / #17 Martin will answer the questions wrong, by voice, and the selector certifies it.** *Concede the mechanism, defend the need.* Any approach that depends on twelve self-reported answers fails this way; but "let the agent judge" fails too, silently. Resolution: the facts are **inferred from the repo with evidence** (an LLM SDK in the lockfile, a `tenant_id` column, a `send_email` tool, a deploy config, tables with names/emails) and shown as "this is what I found, correct me" — one screen, not a questionnaire. `audit-repo-against-kb.md` §Step 1 already does this read-only; we extend it, we do not replace it.

**#4 The `llm` ladder is not cumulative.** *Concede.* Resolution: independent booleans (`llm_calls`, `retrieval`, `tools`, `multi_agent`), plus `acts_on_world` for irreversible side effects, which is what the attack's Content-Central example shows is the real safety trigger (publishing with one LLM call is riskier than a chat agent that only reads).

**#5 / #16 The grammar and the deterministic script are over-engineering with no mechanical consumer.** *Concede.* Nothing downstream is mechanical; the agent applies judgment at every step. Resolution: `applies-when` is a **one-line plain-English predicate over a controlled vocabulary of fact words**, evaluated by the model. The only mechanical check is a grep: the field exists and uses only vocabulary words.

**#6 / #7 `worktrees/` and `spec-driven/` are workflow facts / per-change tests.** *Concede.* Resolution: `parallel_sessions` is one workflow fact that is *asked*, not inferred (the only question). SDD is working-style (`always`); its brownfield branch is a variant chosen by `stage` — the v1 rule "variants only from stack" is dropped.

**#8 The risk formula never discriminates on Martin's portfolio.** *Concede.* Resolution: no formula. Working-style practices keep the existing recommended order in `practices/README.md`; capability practices are ordered by a stated list: `acts_on_world` → `personal_data`/`regulated` → `multi_tenant` → `production` → the rest.

**#9 `rigor` defaults to 1, so the security practices for the fintech and the SaaS never attach.** *Concede — this was the worst flaw.* Resolution: no rigor levels. Security and safety practices attach on **observable facts** (`acts_on_world`, `multi_tenant`, `personal_data`, `regulated`), so the default is the safer one and nobody has to "raise a level".

**#10 "Skipped, reason pasted from prose" is not a technical reason.** *Concede.* Resolution: the agent writes the reason *about this repo* ("no retrieval: no vector store, no embeddings call, no document corpus found"), exactly as the audit playbook already requires ("quote the condition").

**#13 KB-defined files and a re-trigger rule in target repos violate decision 0001.** *Concede.* Resolution: nothing from the KB is written into a target repo by the selector. The facts and the resulting list are the *audit's output* (a markdown block Martin can paste into the repo's own `docs/` or harness changelog if he wants). No schema file, no rule, no hash.

**#14 The signal belongs in `practices/README.md`, which the agent already reads first.** *Concede.* Resolution: one column "Applies when" in that table (≈25 lines at 25 practices) is the progressive-disclosure form; frontmatter carries the same line for consistency.

**#18 Wrong first thing: the existing audit has never been run.** *Concede the order.* Resolution: the deliverable of this change is the smallest version that lets the audit run well, and the **first real iteration is running it on AI SDR** (next step, needs Martin's go, because it touches another repo).

## Round 2 — where I push back

**#15 "Build golden-path bundles instead."** *Partly.* Golden paths are the right *end state* for **new** projects, and the research supports it. But all five of Martin's repos are brownfield, and bundles only pay off when a shape has at least two real instances; building bundles now would be building on zero iterations — the same objection as #18. Resolution: define Martin's **project shapes as worked examples** in the decision guide (facts → practice list) now; promote a shape to a copyable bundle only after it has been applied to two repos.

**#16 "A paragraph read by the model does the same job as a rule."** *Partly.* A paragraph is enough *per practice*; what it does not give is **consistency across 25 practices written by different agents over six months** — the same fact called "multi-tenant", "several customers", "tenants" in three READMEs. The controlled vocabulary (ten words, one file) is the cheapest fix that keeps the model as evaluator. It is not a grammar.

**#12 "No maintenance story."** *Partly conceded.* Resolution: `ingest-new-source.md` gains one step (a new practice must declare `applies-when` in vocabulary words and get its README row); adding a vocabulary word is a change to one file plus a change-log line; `kb-check.sh` greps for undeclared words. That is the whole story, and it is small because the design is small.

**"Is anything conditional at all, then?"** Yes — and this is why the selector is still worth having: the 14 practices coming from the course (RAG pipeline, vector store, chunking, guardrails, multi-agent security, LLMOps…) are conditional in a way the first ten were not. Without an explicit applicability line, an agent auditing the RSS pipeline will be told to add a vector store.

## Agreed design v2 (what gets built now)

1. **Two kinds of practices**, declared in frontmatter `kind: working-style | capability`. Working-style = applies to any repo an agent works in (the current ten, `worktrees/` conditioned on `parallel_sessions`). Capability = attaches by product facts.
2. **Fact vocabulary**, one file `practices/facts.md`: `llm_calls`, `retrieval`, `tools`, `multi_agent`, `acts_on_world`, `multi_tenant`, `production`, `personal_data`, `regulated`, `parallel_sessions`, `brownfield`. Each with: definition, how the agent infers it from the repo (evidence to look for), and whether it is inferred or asked. Adding a word = editing this file + a change-log line.
3. **`applies-when`** in every practice README's frontmatter *and* as a column in `practices/README.md`: one line, plain English, using only vocabulary words (`always`, `retrieval`, `tools or multi_agent`, `multi_tenant and production`…). Evaluated by the agent. Prose "Applies when / Does not apply when" stays for the technical reason.
4. **Ordering**: working-style keeps the existing recommended order; capability practices ordered `acts_on_world → personal_data/regulated → multi_tenant → production → rest`. Stated as a list in `practices/README.md`.
5. **`playbooks/which-practices-apply.md`** — the day-one decision guide: infer the facts with evidence → confirm with Martin in one screen → list applies / skipped-with-repo-specific-reason → hand to `audit-repo-against-kb.md`. Includes three worked examples from Martin's real shapes (multi-tenant agent SaaS; scheduled LLM publishing pipeline; content/marketing site). Nothing written into the target repo.
6. **`audit-repo-against-kb.md`** Step 1 gains the fact inference; Step 3 uses the vocabulary.
7. **`ingest-new-source.md`** gains the "new practice declares `kind` + `applies-when`" step.
8. **`kb-check.sh`**: every practice README has `kind` and `applies-when`; `applies-when` uses only words from `practices/facts.md`; `practices/README.md` table has a row per practice folder.
9. **`decisions/0003-applicability-by-facts.md`**: records this debate and confirms 0001 unchanged.
10. **Not built**: profile schema file, grammar, evaluator script, rigor levels, risk formula, fixtures, re-trigger rule, golden-path bundles (deferred until a shape has two instances).

**Next real step after this lands**: run `which-practices-apply.md` + `audit-repo-against-kb.md` on AI SDR — the first iteration the devil's advocate rightly asked for. Requires Martin's go because it reads another repo.
