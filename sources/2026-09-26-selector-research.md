---
title: "Web research — how authoritative engineering organisations make best-practice catalogues conditional on project characteristics (AWS lenses, Google SRE, OWASP, NIST profiles, Thoughtworks, IDP scorecards, Azure workload guides, coding-agent rules)"
type: source
status: current
date: 2026-09-26
tags: [research, applicability, selector, well-architected, asvs, samm, nist-rmf, scorecards, golden-paths, skills, rules]
sources:
  - (URLs cited inline)
supersedes: null
superseded-by: null
---

# How authoritative engineering organisations make a best-practice catalogue *conditional* on project characteristics

Research note, 2026-09-26. Web research (WebSearch/WebFetch) for the AI Engineering KB. Goal: find the pattern for a "guiding star" knowledge base that a project consults on day one, answers a short self-assessment, and gets back **only the practices that apply**, in a form a coding agent (Claude Code reading markdown) can evaluate.

All claims below are sourced by URL. Where a page was unreachable or only partially readable, that is said explicitly. Opinions are marked as such.

---

## 0. Executive summary (the pattern, in one paragraph)

Every mature catalogue examined separates a **small, universal core** ("pillars", "functions", "factors", a 200-line `CLAUDE.md`) from **conditional overlays** that are attached to a project by an explicit **profile** of that project ("lens", "perspective", "workload guide", "profile", "level", "filter", "paths glob", "SKILL description"). Applicability is never inferred from prose; it is decided by (a) a handful of typed dimensions in a metadata record, (b) a chosen rigor level, or (c) a boolean rule over those two. The catalogue is consumed through a **questionnaire → gaps → risk-ranked improvement plan** loop (AWS WA Tool, Azure assessments, SAMM, Cortex/OpsLevel scorecards), with an explicit **"not applicable / skipped"** state that is distinct from "failed" (GitLab, ASVS, Cortex exemptions). The documented failure modes are the same everywhere: checklist creep (Google LCE), everything-applies (Cortex: "a standard that's obviously wrong for some entities loses credibility fast"), stale overlays (AWS lenses revised yearly; Thoughtworks blips expire after one edition), and false precision (NIST: "silence doesn't indicate irrelevance"; ASVS: picking L2 "because it is the middle number").

---

## 1. Model-by-model findings

### 1.1 AWS Well-Architected Framework: pillars + lenses + the WA Tool

**How applicability is decided.** Two mechanisms stacked:

1. *Lens attachment.* The base Framework Lens (6 pillars) is "automatically applied when a workload is defined"; a workload "can have one or more lenses applied", up to 20, each lens carrying "its own set of questions, best practices, notes, and improvement plan" ([WA Tool user guide, lenses](https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses.html)). Lenses are workload-type overlays: SaaS, Serverless, Generative AI, Machine Learning, etc. The person running the review picks which lenses apply; there is no automatic profile → lens inference.
2. *Risk rules inside a lens.* Each question has choices; risk is computed by ordered boolean rules over choice IDs. The custom-lens JSON spec (verbatim) ([lens format specification](https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses-format-specification.html)):

   ```json
   "riskRules": [
     { "condition": "choice_1 && choice_2 && choice_3", "risk": "NO_RISK" },
     { "condition": "((choice_1 || choice_2) && choice_3) || (!choice_1 && choice_3)", "risk": "MEDIUM_RISK" },
     { "condition": "default", "risk": "HIGH_RISK" }
   ]
   ```
   Limits: ≤10 pillars per lens, ≤20 questions per pillar, ≤15 choices per question, ≤3 risk rules per question, a `_no` choice suffix meaning "None of these". Every non-`_no` choice must carry an `improvementPlan.displayText`. This is the most concrete "questionnaire → risk → plan" schema found in this research and is directly reusable as a design reference.

**How the SaaS Lens handles multi-tenancy.** The lens explicitly scopes itself: "For brevity, we have only covered details from the Well-Architected Framework that are specific to SaaS workloads. You should still consider best practices and questions that have not been included" ([SaaS Lens](https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/saas-lens.html)). It adds 14 SaaS-specific design principles, of which the multi-tenancy ones are: "decompose each service based on its multi-tenant load and isolation profile" (pooled vs siloed), "isolate all tenant resources", "bind user identity to tenant identity", "plan to support multiple tenant experiences" (tiering), "instrument, capture, and analyze tenant metrics", "measure the cost impact of individual tenants", and "limit developer awareness of multi-tenant concepts" ([general design principles](https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/general-design-principles.html)). So multi-tenancy is not a yes/no flag inside the base framework; it is a *separate overlay*, and inside that overlay the questions themselves branch on the isolation model (silo/pool/bridge) and tiering.

**Generative AI Lens (2025).** Scope statement is by platform ("generative AI applications using foundation models on Amazon Bedrock or customer-managed models on SageMaker AI"), organised by the six pillars *and* by a six-stage lifecycle (scoping, model selection, customization, development, deployment, continuous improvement). It explicitly hands off traditional ML to the ML Lens ([Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html); [announcement](https://aws.amazon.com/about-aws/whats-new/2025/04/well-architected-generative-ai-lens)). This is the "one lens per technology, cross-cut by the pillars" pattern.

**Catalogue organisation.** Pillar → question → best practice (each with an ID such as `SEC01-BP01`, `GENOPS01`) → improvement plan. Stable IDs are what make the catalogue referenceable by tools and by other documents.

**Kept current.** Lenses are versioned; the WA Tool retains answers when a lens is removed and re-added, and lens upgrades are explicit operations. Official lenses are revised roughly yearly (the GenAI lens was updated within a year of launch, per the AWS Architecture Blog announcement pages).

**Consumed by.** Humans in the WA Tool console; also programmatically via the WA Tool API and custom lens JSON. Not designed for an LLM, but the JSON is trivially machine-readable.

**Known weaknesses.** (a) Lens selection is manual and there are 20+ lenses; nothing stops you from applying none or all. (b) Reviews degrade into "a checkpoint exercise that generates a PDF nobody reads" unless scoped to one workload ([practitioner write-up](https://dev.to/instadevops/how-to-run-an-aws-well-architected-review-the-6-pillars-and-common-findings-3p15)). (c) Only three risk levels and a `_no` choice: "not applicable" is not first-class at the choice level, only at the question level via the tool's "Question does not apply" toggle. (d) Vendor-shaped: the GenAI Lens is scoped by AWS products, not by workload characteristics.

### 1.2 Google SRE: Production Readiness Review, Launch Checklist, Cloud Architecture Framework

**PRR.** The "simple PRR model" is engagement → analysis (checklists plus domain expertise) → improvements → training → onboarding ([SRE book, Evolving SRE engagement model](https://sre.google/sre-book/evolving-sre-engagement-model/)). Applicability is decided by *humans with a checklist*, not by metadata. Google's own stated weakness: "additional communication between teams can increase some process overhead for the development team, and cognitive burden for the SRE reviewers", and the review comes too late. Their fix was structural, not a better checklist: **frameworks** ("built and blessed by SRE") so that a service inherits the standards by construction, cutting onboarding to "one quarter". Translated: the best applicability engine is a template that already embodies the practice (see Spotify Golden Paths, §1.6).

**Launch Coordination Checklist.** Nine question domains (architecture, machines/datacenters, capacity, reliability/failover, monitoring, security, automation, growth, external dependencies), each entry in "question + action item" form ([launch checklist appendix](https://sre.google/sre-book/launch-checklist/)). The governance is the interesting part ([Reliable product launches](https://sre.google/sre-book/reliable-product-launches/)): "Every question's importance must be substantiated, ideally by a previous launch disaster" and "every instruction must be concrete, practical, and reasonable for developers to accomplish". Adding a question once required VP approval. Annual full review to delete obsolete items. Stated failure mode: "there is a near-infinite number of questions to ask about any system, and it is easy for the checklist to grow to an unmanageable size"; "engineers are likely to sidestep processes that they consider too burdensome". The original checklist is from ~2005 and has no per-launch tailoring rules; tailoring was the LCE's job.

**Google Cloud Well-Architected Framework.** Six pillars plus **perspectives**, defined as "a cross-pillar view of recommendations for a specific technology, domain, or sector" (AI and ML; Financial Services) ([framework overview](https://docs.cloud.google.com/architecture/framework); [AI and ML perspective](https://docs.cloud.google.com/architecture/framework/perspectives/ai-ml)). Same shape as AWS lenses, without a questionnaire tool.

**Weaknesses.** PRR does not scale without dedicated SREs (Google says so). The checklist has no machine-readable applicability. Perspectives have no assessment tooling.

### 1.3 OWASP: ASVS levels, SAMM maturity, LLM/Agentic Top 10

**ASVS 5.0 (May 2025).** ~350 requirements in 17 chapters, three cumulative levels. 5.0 reframed the levels: L1 is "the initial step to adopting the ASVS, providing the first layer of defense", L2 "a comprehensive view of standard security practices", L3 "advanced, high-assurance requirements" ([ASVS 5.0 preface](https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x02-Preface.md)). Level selection is risk-driven (data sensitivity, financial impact, regulation, adversary attractiveness); L2 is the recommended target for "SaaS products, e-commerce, customer portals and systems processing personal data" ([Breachroad guide](https://breachroad.com/en/blog/owasp-asvs-5-levels-implementation/)). Two applicability rules worth copying verbatim from that guide: "not every component must automatically receive the same profile" and "Mark a requirement not applicable only with a technical explanation. The absence of password recovery can justify excluding recovery-specific controls; lack of implementation time cannot." Documented decisions are now part of the standard ("requirements now include documentation of key security decisions").

*Weakness.* Levels are a single scalar; they encode rigor, not shape. Common misuse: choosing L2 "because it is the middle number", which "typically leads to program abandonment within a year" ([SecureCodingHub](https://www.securecodinghub.com/blog/owasp-asvs-developers-complete-guide)). The chapter structure does the "shape" filtering implicitly (no OAuth chapter if you have no OAuth), which is only as good as the reader's honesty.

**SAMM.** 5 business functions × 3 practices × 2 streams × 3 maturity levels; assessed by questionnaire; "SAMM does not insist that all organizations achieve the maximum maturity level in every category" — you set a **target posture per practice** and derive a roadmap ([SAMM model](https://owaspsamm.org/model/); [about](https://owaspsamm.org/about/)). Pattern: per-topic target levels, not one global level. *Weakness:* organisation-level, process-heavy; too coarse for a single repo.

**LLM Top 10 (2026) and Top 10 for Agentic Applications (2026).** The agentic list (ASI01 Goal Hijack … ASI10 Rogue Agents) is scoped to systems that "plan and execute multi-step tasks", use tools/APIs, hold memory, and run in multi-agent ecosystems ([OWASP GenAI project](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/); [Teleport summary](https://goteleport.com/blog/owasp-top-10-agentic-applications/)). The LLM list applies to "applications powered by large language models" generally and maps its items onto the agentic list ([LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)). So OWASP is de facto using **capability flags** as the applicability gate: `uses_llm` → LLM Top 10; `agent_with_tools || memory || multi_agent` → Agentic Top 10 in addition. Neither document ships a questionnaire; the gate is the reader's self-classification.

*Weakness.* Top-10 lists are awareness documents, not verification standards; there is no L1/L2/L3 within them, so "applies" means "read all ten". OWASP's AISVS is the attempt to add levels for AI ([AISVS](https://owasp.org/projects/artificial-intelligence-security-verification-standard-aisvs-docs)).

### 1.4 NIST AI RMF profiles

A profile is "an implementation of the AI RMF's functions, categories, and subcategories for a specific setting or technology" ([CASRAI guide to AI 600-1](https://casrai.org/guides/nist-ai-rmf-generative-ai-profile)). NIST names three kinds: use-case profiles, temporal (current vs target) profiles, and cross-sectoral profiles. The Generative AI Profile (AI 600-1, July 2024) is cross-sectoral: it names 12 GAI-specific risks and tags each suggested action `GV-1.1-001`-style to a base subcategory plus the risks it addresses. Two honest limits stated by NIST: it is a *partial* map ("not every subcategory of the AI RMF is included in this document") and "silence doesn't indicate irrelevance".

The CSA's draft **Agentic profile** ([CSA labs](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)) defines "what counts as agentic" by five characteristics (autonomous execution, tool use, multi-step planning, delegation, persistent effects) and introduces a **four-tier autonomy classification** with escalating obligations, plus a per-tool risk inventory (consequence scope, reversibility, composition risk). That is a clean example of a profile whose *dimensions* (autonomy tier, tool reversibility) drive which controls attach.

*Weaknesses.* Volume (hundreds of suggested actions), non-prescriptive, no verification method, and the "current vs target profile" idea has no tooling.

### 1.5 Thoughtworks: Technology Radar and Sensible Defaults

**Radar.** Four quadrants × four rings; rings are recommendation strength ("Adopt: … proven and mature for use"; "Trial: ready for use, but not as completely proven"; "Assess: … look at closely, but not necessarily trial yet"; "Hold" for bad experiences). Blips are crowdsourced, debated twice a year by ~20 people, and **expire**: "Blips only appear on the Radar for one edition unless they move rings" ([Radar FAQ](https://www.thoughtworks.com/radar/faq)). Applicability is *not* per project; the Radar is a currency mechanism, and Thoughtworks tells you to "build your own radar".

**Sensible defaults.** "Something that, in most circumstances, should be done in the absence of any other specific options or approaches"; "Sensible defaults aren't dogma … if they aren't suitable, we always make a conscious decision not to follow them" ([Thoughtworks blog](https://www.thoughtworks.com/insights/blog/technology-strategy/better-tech-decision-making-underpinned-by-sensible-defaults)). Applicability = default-on with **documented opt-out**, curated by communities of practice. Stated weakness: "Sensible defaults require technical maturity."

*Takeaway.* Two distinct axes that other frameworks conflate: **recommendation strength** (adopt/trial/assess/hold, with an expiry clock) and **applicability** (default unless justified). Both are worth having as separate fields.

### 1.6 Backstage / Spotify Golden Paths, Cortex and OpsLevel scorecards, GitLab maturity model

**Backstage catalog metadata.** `catalog-info.yaml` gives every entity `kind` (Component/System/API/Resource/Domain), `spec.type` (service/website/library…), `spec.lifecycle` (experimental/production/deprecated), `spec.owner`, `tags`, `labels`, `annotations` and relations ([descriptor format](https://backstage.io/docs/features/software-catalog/descriptor-format/)). This is the industry's de facto **project profile schema**. Tech Insights checks are `json-rules-engine` rules over "facts"; fact retrievers take an `entityFilter` such as `[{ kind: 'component' }]`, and checks are scoped by which retrievers produced facts for the entity ([tech-insights backend README](https://github.com/backstage/community-plugins/blob/main/workspaces/tech-insights/plugins/tech-insights-backend/README.md)).

**Golden Paths.** "The opinionated and supported path to build" per discipline (backend service, web app, data pipeline, client, data science, ML, audio); "if you are an adventurer you can of course leave the Golden Path … but then you will not have the same support"; kept current by forcing every new hire through the tutorial in their first two weeks ([Spotify engineering](https://engineering.atspotify.com/2020/08/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem)). Applicability = one path per *software type*; the path is a template, so practices are inherited rather than checked.

**Cortex scorecards.** Rules are testable claims ("the entity has a Datadog monitor attached"), written in CQL. Two scoring modes: **levels/ladders** (Bronze/Silver/Gold, must pass all rules in a level and below; "suits maturity models and production readiness") and **points**. Scorecards are scoped by entity type, groups or CQL; **rule-level filters** narrow individual rules; **exemptions** make a rule "neither passing nor failing". The doc's own rationale: "a standard that's obviously wrong for some entities loses credibility fast." Initiatives add deadlines ([Cortex scorecards](https://docs.cortex.io/standardize/scorecards.md)).

**OpsLevel.** "Filters let you define which of your services each Check should apply to based on service properties" (tier, lifecycle, tags, language, owner, system); checks sit in a rubric of levels × categories; a "Matching Services" preview shows the blast radius of a filter before it ships; filters nest only one level ([OpsLevel checks and filters](https://docs.opslevel.com/docs/checks-and-filters)).

**GitLab Service Maturity Model.** A real scaling issue: infra-only services (PgBouncer) fail "developer documentation" criteria that make no sense for them. The proposed fix: externalise criteria, let each service catalog entry declare excluded criteria (validated against the criteria list), and change the result from `passed` boolean to `passed | failed | skipped | not_implemented` ([GitLab issue 826](https://gitlab.com/gitlab-com/gl-infra/scalability/-/issues/826)). This four-state result is the cleanest answer found to "how do we represent not-applicable honestly".

*Weaknesses (all three).* They evaluate what integrations can see (does a monitor exist), not whether practices are actually sound; metadata rots ("tier" is set once); scorecards become gamed. Backstage's own scorecards are a community plugin, not core.

### 1.7 12-Factor App / 12-Factor Agents; Azure Well-Architected workload guides and agent patterns

**12-Factor Agents** (HumanLayer): twelve factors (own your prompts, own your context window, tools are structured outputs, unify execution and business state, launch/pause/resume, contact humans with tool calls, own your control flow, compact errors, small focused agents, trigger from anywhere, stateless reducer). Explicitly a pick-list, not a checklist: "take small, modular concepts from agent building" into existing products ([12-factor-agents](https://github.com/humanlayer/12-factor-agents)). No applicability rules at all; every factor is "consider".

**Azure Well-Architected workload guides.** Pillars are generic; each **workload guide** (AI, SaaS, mission-critical, …) has design methodology → design principles → design areas → assessment. Applicability is decided by an explicit **in/out-of-scope statement** at the top. AI guide: out of scope are "workloads that are realized through low-code and no-code offerings, such as Copilot Studio", HPC, and "workloads that don't implement generative or discriminative AI use cases" ([AI workload guide](https://learn.microsoft.com/en-us/azure/well-architected/ai/get-started)). SaaS guide: for ISVs selling B2B/B2C, both startups and established firms; "not intended for organizations building software for internal use only"; nine design areas, with multitenancy framed as "a core business methodology" and isolation as the critical requirement ([SaaS workload guide](https://learn.microsoft.com/en-us/azure/well-architected/saas/get-started)). The assessment is a multiple-choice questionnaire per design area that yields "technical recommendations tailored to your responses" and "prioritized guidance" ([AI assessment](https://learn.microsoft.com/en-us/azure/well-architected/ai/assessment)).

**Azure AI agent orchestration patterns.** Five patterns (sequential, concurrent, group chat, handoff, magentic), each with explicit "Use when / Avoid when" bullets and a comparison table with a "Watch out for" column, preceded by the rule "Use the lowest level of complexity that reliably meets your requirements" and the progression direct model call → single agent with tools → multi-agent ([Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)).

*Weaknesses.* Workload guides overlap (an AI SaaS product must read two guides with no merge rule). Scope statements are prose, not machine-checkable. Pattern guides tell you when a pattern fits but not how to record the decision.

### 1.8 Anthropic / OpenAI decision guides for agents

**Anthropic, Building Effective Agents** (Dec 2024). Rule zero: "find the simplest solution possible, and only increasing complexity when needed"; workflows give "predictability and consistency for well-defined tasks", agents "flexibility and model-driven decision-making". Each pattern carries a one-line applicability test: prompt chaining "where the task can be easily and cleanly decomposed into fixed subtasks"; routing "where there are distinct categories that are better handled separately"; parallelization "when the divided subtasks can be parallelized for speed, or when multiple perspectives or attempts are needed"; orchestrator-workers "where you can't predict the subtasks needed"; evaluator-optimizer "when we have clear evaluation criteria, and when iterative refinement provides measurable value"; autonomous agents "for open-ended problems where it's difficult or impossible to predict the required number of steps" ([Anthropic](https://www.anthropic.com/research/building-effective-agents)).

**OpenAI, A Practical Guide to Building Agents** (2025). Build an agent only when one of three conditions holds: "complex decision-making", "difficult-to-maintain rules", "heavy reliance on unstructured data". Start single-agent; split when "prompts contain many conditional statements" or tools overlap ("some implementations successfully manage more than 15 well-defined, distinct tools while others struggle with fewer than 10 overlapping tools"). Guardrails are "a layered defense mechanism"; human escalation for actions that are "sensitive, irreversible, or have high stakes" ([OpenAI PDF](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)).

*Pattern.* Neither vendor uses tags or levels; they use **entry conditions written as short predicates** on the *task*, and a default that is always "the simpler thing". This is the right granularity for a practice's `applies-when` prose line.

### 1.9 Conditional knowledge for coding agents: Skills, Claude Code rules, Cursor rules, AGENTS.md

| Mechanism | Applicability signal | Loaded when | Cost model |
|---|---|---|---|
| Agent Skills `SKILL.md` | `description` (≤1024 chars, "what it does and when to use it", keyword-rich) | Model decides from description; "Metadata (~100 tokens)… loaded at startup for all skills; Instructions (<5000 tokens)… when activated; Resources as needed" | Progressive disclosure; body ≤500 lines ([spec](https://agentskills.io/specification)) |
| Claude Code `.claude/rules/*.md` | `paths:` glob list in frontmatter; "`paths` is the only field Claude Code reads from a rule; any other field is ignored without an error" | "when Claude reads files matching the pattern, not on every tool use"; rules without `paths` load at launch | Unscoped rules "waste tokens by loading context even when it's not relevant" ([memory docs](https://code.claude.com/docs/en/memory); [steering blog](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)) |
| Cursor rules | `alwaysApply: true` (globs and description ignored); `globs` → "auto-attached when a matching file is in context"; `description` only → "agent reads the description and pulls the rule in when relevant"; neither → manual `@` | Per file-in-context / per model judgement | "Keep rules under 500 lines", split into composable rules ([Cursor docs](https://cursor.com/docs/context/rules)) |
| `AGENTS.md` | Directory proximity: "The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything" | Always, for the nearest file | No size rule in the spec ([agents.md](https://agents.md/)) |

Three consequences for our design:

1. Today's coding-agent mechanisms decide applicability by **file path** or by **free-text description matched by the model**. Neither can express "this project is multi-tenant" or "this project has EU users"; those are project-level facts, not path-level facts. A project profile therefore has to live in a file the agent reads at launch (`CLAUDE.md`/`AGENTS.md` pointer → `docs/profile.yml` or similar) and be evaluated by the agent, not by the loader.
2. Anthropic's own guidance says instructions are "context, not enforced configuration"; "a real guardrail needs to be deterministic" (hooks, settings). So the selector should *produce* hooks/tests where possible, not more prose.
3. Everything above enforces a **size budget** (200-line CLAUDE.md, 500-line rules/skills, ~100-token skill metadata). A selector's output must fit those budgets or it will be ignored.

### 1.10 2025–2026 write-ups on standards that agents consume

- Packmind's context-engineering playbook proposes four layers (system prompts, path-scoped rules, lazy-loaded skills, commands), hierarchical scoping (root → module → file type), and names **context drift** ("when the codebase evolves but the instruction files do not follow") as the main maintenance failure; mitigations are periodic audits against the code and "rejection pattern analysis" from code review; "every token in the context window should carry information the agent cannot infer from the code itself" ([Packmind](https://packmind.com/context-engineering-ai-coding/context-engineering-playbook/)).
- arXiv 2603.09619 (2026) frames context engineering with five quality criteria (relevance, sufficiency, isolation, economy, provenance) and layers "specification engineering: a machine-readable corpus of corporate policies and standards enabling autonomous operation" on top ([arXiv](https://arxiv.org/abs/2603.09619)). Useful vocabulary (provenance, economy), no concrete applicability mechanism.
- Practitioner posts on AGENTS.md nesting/overrides (e.g. [Codex KB](https://codex.danielvaughan.com/2026/03/26/agents-md-advanced-patterns/), [DEV](https://dev.to/promptmaster/agentsmd-in-a-monorepo-nested-files-and-precedence-1b7d)) all converge on: closest-file precedence, keep the root short, push specifics down the tree. None found addresses project-characteristic applicability beyond path scoping.

Nothing found in 2025–2026 describes a project-profile-driven selector for markdown practices. This appears to be a gap; the closest analogues are the IDP scorecard filters (§1.6) and the AWS custom-lens JSON (§1.1).

---

## 2. Comparison table

| Model | Applicability decided by | Catalogue organisation | Kept current by | Consumed by | Main weakness |
|---|---|---|---|---|---|
| AWS Well-Architected + lenses + WA Tool | Manual lens attachment per workload; boolean `riskRules` over questionnaire choices | Pillar → question → best-practice ID → improvement plan; ≤20 lenses/workload | Versioned lenses, ~yearly revisions, answer retention | Human console; JSON/API | Lens choice manual; reviews become PDF theatre; vendor-scoped |
| Google SRE PRR / launch checklist | Human reviewers with a checklist; later: frameworks that embody standards | 9 domains of "question + action" | "Substantiated by a previous launch disaster"; annual prune; VP gate on additions | Humans (LCE/SRE) | Does not scale without SREs; checklist creep |
| Google Cloud Architecture Framework | Reader picks perspective (AI/ML, FS) | Pillars × perspectives | Doc updates | Humans | No assessment tooling |
| OWASP ASVS 5.0 | Chosen rigor level (L1–L3, cumulative); chapter relevance; documented N/A with technical reason | 17 chapters × ~350 requirements × level flag | Major versions (4.0→5.0, 2025) | Humans/auditors; CSV/JSON exports | Level is one scalar; "pick L2 because middle" |
| OWASP SAMM | Per-practice target maturity | 5×3 practices × 2 streams × 3 levels | Versioned model + toolbox | Humans (interviews) | Org-level, heavy |
| OWASP LLM / Agentic Top 10 (2026) | Self-classification: uses LLM? has tools/memory/multi-agent? | Two flat lists, cross-mapped | Yearly editions | Humans | Awareness lists, no levels, "read all ten" |
| NIST AI RMF profiles | Profile per use case/sector; CSA agentic profile adds autonomy tiers, tool reversibility | Functions → categories → subcategories → tagged actions | New profiles (GenAI 2024, agentic draft) | Humans/compliance | Volume; non-prescriptive; partial maps |
| Thoughtworks Radar / Sensible defaults | Radar: none (strength only). Defaults: on-unless-justified | Quadrants × rings; defaults by community | Blips expire after one edition; 6-month cadence | Humans | Not per project; needs maturity |
| Backstage / Cortex / OpsLevel / GitLab | Entity metadata (kind, type, lifecycle, tier, tags) + filters/CQL; exemptions; `skipped` state | Scorecards: levels or points; rules per level | Continuous evaluation; initiatives with deadlines | Automated (facts from integrations) | Measures presence, not quality; metadata rot; gaming |
| Spotify Golden Paths | One path per software type; opt-out loses support | Tutorials/templates per discipline | New hires walk the path in week 1–2 | Humans via templates | Only as current as the template |
| 12-Factor Agents | None (pick what helps) | 12 factors | Community | Humans | No applicability at all |
| Azure WAF workload guides + agent patterns | Prose in/out-of-scope statement; "Use when / Avoid when" per pattern; assessment questionnaire | Methodology → principles → design areas → assessment | Doc updates | Humans; assessment web tool | Overlapping guides; scope not machine-checkable |
| Anthropic / OpenAI agent guides | Short predicates on the task; default = simplest thing | Pattern list with entry conditions | Rewrites | Humans | No recording mechanism for the decision |
| Skills / Claude rules / Cursor rules / AGENTS.md | `description` matched by model; `paths`/`globs`; `alwaysApply`; nearest file | Files with frontmatter; progressive disclosure | Repo commits | Coding agents | Only path- or description-level; no project-level facts; size budgets |

---

## 3. Recurring design principles

1. **Small universal core + attachable overlays.** Pillars/functions/factors are few and always apply; everything specific is an overlay attached by an explicit choice (AWS lens, Google perspective, Azure workload guide, NIST profile, OWASP Top-10 variant). Overlays are cross-cut by the core (GenAI lens is still organised by the six pillars) so they never become a second, competing taxonomy.
2. **Two separate axes: shape and rigor.** Shape = what kind of system this is (multi-tenant, has agents, has RAG). Rigor = how much assurance (ASVS L1–L3, SAMM target level, Cortex Bronze/Silver/Gold, CSA autonomy tier). Frameworks that collapse them into one number get misused ("L2 because middle"). Rigor should be settable per topic, not globally (SAMM).
3. **Questionnaire → gaps → risk-ranked improvement plan**, with every choice tied to a concrete improvement (AWS requires `improvementPlan` per choice; Google requires "question + action item"; Azure returns "prioritized guidance"). A finding without an action is not allowed into the catalogue.
4. **Metadata-driven applicability, with honest N/A.** IDP scorecards decide by typed entity fields plus boolean filters, allow rule-level filters and exemptions, and GitLab's four-state result (`passed | failed | skipped | not_implemented`) separates "doesn't apply" from "not done". ASVS adds: N/A needs a *technical* reason.
5. **Entry conditions as short predicates; default to the simplest thing.** Anthropic/OpenAI/Azure all write "use when / avoid when" in one or two lines and bias toward the least complex option.
6. **Aggressive curation with an expiry clock.** Google: substantiated by a disaster, VP gate, annual prune. Thoughtworks: blips expire after one edition. AWS: versioned lenses. Every catalogue that survived says the same: the enemy is growth.
7. **Prefer inheritance and enforcement over prose.** Google frameworks and Spotify Golden Paths make the practice the default by construction; Anthropic says instructions are "context, not enforced configuration" and real guardrails are hooks. A selector should end by generating hooks, tests and templates, not paragraphs.
8. **Context budget is a hard constraint for agents.** 200-line entry file, 500-line rules/skills, ~100-token metadata, load-on-demand. Whatever the selector emits has to fit.

---

## 4. Recommendations for our KB ("guiding star")

### 4.1 Project profile schema

Keep it to the dimensions that actually change which practice applies. Every dimension must be cited by at least one practice's `applies-when`; a dimension nobody uses gets deleted (Google's rule, applied to questions). Proposed first version, as `docs/project-profile.yml` in the target repo (agent reads it at launch via a one-line pointer in `CLAUDE.md`/`AGENTS.md`):

```yaml
# docs/project-profile.yml  — answered once on day one, re-answered when it changes
schema: 1
stage: greenfield | brownfield          # is there existing code/users to protect?
traffic: none | internal | production   # real users hitting it?
team: solo | small | multi-team
tenancy: single | multi                 # multiple customers sharing one deployment?
data: none | personal | regulated       # PII / payments / health
regions: [mx, us, eu]                   # EU triggers GDPR-related practices
ui: none | api | web | chat             # chat = conversational surface exists
llm: none | calls | rag | agent-tools | multi-agent   # cumulative ladder
autonomy: 0 | 1 | 2 | 3                 # CSA-style: 0 no actions, 3 unsupervised irreversible actions
stack: {lang: ts, runtime: node, hosting: digitalocean}   # picks practice variants, not applicability
rigor: {security: 1|2|3, reliability: 1|2|3, agent-safety: 1|2|3}   # per-topic target, SAMM-style
exemptions:                              # ASVS rule: technical reason required
  - practice: worktrees
    reason: "single developer, single branch at a time"
```

Rules for the schema: ≤12 dimensions; each is an enum (no free text, so a boolean expression can evaluate it); `stack` selects *variants* (which file to copy), never applicability; `rigor` is per topic; `exemptions` are explicit and reasoned.

### 4.2 How practices declare applicability

Add three fields to the existing practice/principle frontmatter (the KB already has prose "Applies when / Does not apply when"; keep that prose for humans and add the machine form):

```yaml
applies-when: "llm in [agent-tools, multi-agent] and traffic == production"
strength: default | recommended | consider      # Thoughtworks-style; 'default' = on unless exempted
rigor-min: {agent-safety: 2}                    # only attach when the target rigor is at least this
```

Design choices, with reasons:

- **Boolean expression over profile enums, not tags.** Tags only express OR; the interesting cases are ANDs and negations ("multi-tenant AND production", "agent-tools AND NOT solo"). AWS `riskRules` and Cortex CQL both use expressions; OpsLevel found tag-style filters needed composition and still capped nesting at one level. Keep the grammar tiny: `==`, `!=`, `in`, `and`, `or`, `not`, parentheses. It must be readable by a human and evaluable by an agent without a parser (the agent can reason over it) *and* by a 30-line script in `scripts/` (so `kb-check.sh` can validate that every expression references only declared dimensions and every dimension is referenced).
- **`strength` separate from applicability**, so a practice can apply but be "consider" (12-factor style) rather than "default".
- **Levels only where they earn their keep.** Three topics have a natural rigor ladder in the sources (security via ASVS, reliability via readiness ladders, agent safety via CSA autonomy tiers). Do not add levels elsewhere.
- **Keep the prose "Does not apply when" section**; it is where the ASVS-style *technical reason* templates live, and it is what the agent quotes when it marks something `skipped`.

### 4.3 How a coding agent should evaluate it (the day-one playbook)

1. **Read `docs/project-profile.yml`.** If missing, run the questionnaire: ≤12 questions, one per dimension, each with the enum choices and one sentence explaining why it matters (Azure/AWS style). Write the file; stop for approval (matches the KB's "investigation before implementation" rule).
2. **Evaluate every practice's `applies-when`** against the profile. Produce a table with four states, GitLab-style: `applies (default)`, `applies (consider)`, `skipped (reason)`, `exempt (reason from profile)`. Never "everything applies": `kb-check.sh` should fail if the universal core exceeds a fixed count (say 6 practices) or if any practice has no `applies-when` at all.
3. **Order by risk, not by catalogue order.** Borrow AWS's three-level risk: a `default` practice that is absent in a `production` + `personal data` profile is HIGH; absent `consider` practices are informational. Present the plan; stop for approval.
4. **Apply through the existing practice folders** (copy files, replace placeholders, run Verify), and prefer generating hooks/tests/templates over adding prose (principle 7 above). Record the profile hash and the list of applied/skipped practices in the repo's harness changelog so a later audit can diff.
5. **Re-run when the profile changes** (e.g. `traffic: internal → production`, `llm: rag → agent-tools`). The profile file is the trigger; a path-scoped `.claude/rules/profile.md` with `paths: ["docs/project-profile.yml"]` can remind the agent to re-run the selector whenever it touches that file.

Loading budget: the selector's output into the target repo should be ≤1 pointer line in `CLAUDE.md`, one profile file, and path-scoped rules or skills for the rest, per the 200/500-line limits above.

### 4.4 Failure modes to design against (each with the source that documented it)

- **Questionnaire fatigue.** AWS reviews become "a PDF nobody reads"; Google engineers "sidestep processes that they consider too burdensome". Cap the profile at ~12 enum questions, answerable in ten minutes, and never ask a question that no practice reads.
- **Everything-applies.** Cortex: "a standard that's obviously wrong for some entities loses credibility fast". Enforce with `kb-check.sh`: universal core ≤ N; every practice has `applies-when`; run the selector against three fixture profiles (solo greenfield API, multi-tenant production SaaS with agents, EU chat product) and fail if the first fixture gets more than ~8 practices.
- **Stale overlays / context drift.** AWS re-versions lenses; Thoughtworks expires blips; Packmind names drift explicitly. The KB already has `last-reviewed`; add a check that any practice not reviewed in 12 months is flagged in the selector output as "review before applying" (Google's annual prune, automated).
- **False precision.** NIST: "silence doesn't indicate irrelevance"; ASVS: choosing a level by its number. Mitigations: profile values are coarse enums, not scores; the selector output states what it did *not* evaluate; rigor defaults to 1 and must be raised deliberately with a reason.
- **Metadata rot.** IDP scorecards decay because `tier` is set once. Store the profile in the repo, version it, and make the audit playbook re-ask only the dimensions whose evidence contradicts the file (e.g. a `tenant_id` column in migrations but `tenancy: single`).
- **Prose as guardrail.** Anthropic: instructions are "context, not enforced configuration". Every `default` practice with a mechanical check should ship its hook/test; the selector reports which applied practices are enforced vs merely documented.
- **Two competing taxonomies.** Azure's AI and SaaS guides overlap with no merge rule. Keep one core (the principles) and make every overlay reference it by ID, as AWS lenses reference pillars.

### 4.5 Where this lands in the current repo (proposal, not done)

- `principles/` gains one principle: *applicability and project profiles* (the "why" of this note), status `draft` until Martin approves.
- `practices/_template/README.md` gains the three frontmatter fields; each existing practice folder gets an `applies-when` line derived from its current prose section.
- templates/project-profile.yml and a questionnaire playbook playbooks/profile-a-repo.md (both rejected in the debate; not built) (day-one entry), which `playbooks/audit-repo-against-kb.md` then calls before auditing.
- `scripts/kb-check.sh` gains the three checks listed in §4.4 (core size, expression validity, fixture profiles). A 30-line `scripts/select-practices.py` evaluates expressions so the check is deterministic.

---

## 5. Sources consulted (primary first)

- AWS: [WA Tool lenses](https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses.html); [custom lens format specification](https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses-format-specification.html); [SaaS Lens](https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/saas-lens.html); [SaaS Lens design principles](https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/general-design-principles.html); [Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html); [GenAI Lens announcement, Apr 2025](https://aws.amazon.com/about-aws/whats-new/2025/04/well-architected-generative-ai-lens); practitioner view: [How to run a WA review](https://dev.to/instadevops/how-to-run-an-aws-well-architected-review-the-6-pillars-and-common-findings-3p15).
- Google: [Evolving SRE engagement model (PRR)](https://sre.google/sre-book/evolving-sre-engagement-model/); [Reliable product launches (LCE)](https://sre.google/sre-book/reliable-product-launches/); [Launch checklist appendix](https://sre.google/sre-book/launch-checklist/); [Cloud Well-Architected Framework](https://docs.cloud.google.com/architecture/framework); [AI and ML perspective](https://docs.cloud.google.com/architecture/framework/perspectives/ai-ml).
- OWASP: [ASVS 5.0 preface](https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x02-Preface.md); [ASVS project page](https://owasp.org/www-project-application-security-verification-standard/); [Breachroad ASVS 5 guide](https://breachroad.com/en/blog/owasp-asvs-5-levels-implementation/); [SecureCodingHub ASVS guide](https://www.securecodinghub.com/blog/owasp-asvs-developers-complete-guide); [SAMM model](https://owaspsamm.org/model/); [SAMM about](https://owaspsamm.org/about/); [Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/); [LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/); [Teleport summary of agentic list](https://goteleport.com/blog/owasp-top-10-agentic-applications/); [AISVS](https://owasp.org/projects/artificial-intelligence-security-verification-standard-aisvs-docs).
- NIST: [CASRAI guide to AI 600-1](https://casrai.org/guides/nist-ai-rmf-generative-ai-profile); [NIST AI 600-1 draft PDF](https://airc.nist.gov/docs/NIST.AI.600-1.GenAI-Profile.ipd.pdf); [CSA Agentic AI RMF profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/).
- Thoughtworks: [Sensible defaults](https://www.thoughtworks.com/insights/blog/technology-strategy/better-tech-decision-making-underpinned-by-sensible-defaults); [Radar FAQ](https://www.thoughtworks.com/radar/faq).
- IDPs: [Backstage descriptor format](https://backstage.io/docs/features/software-catalog/descriptor-format/); [Backstage Tech Insights backend](https://github.com/backstage/community-plugins/blob/main/workspaces/tech-insights/plugins/tech-insights-backend/README.md); [Spotify Golden Paths](https://engineering.atspotify.com/2020/08/how-we-use-golden-paths-to-solve-fragmentation-in-our-software-ecosystem); [Cortex Scorecards](https://docs.cortex.io/standardize/scorecards.md); [OpsLevel checks and filters](https://docs.opslevel.com/docs/checks-and-filters); [GitLab maturity-model exemptions issue](https://gitlab.com/gitlab-com/gl-infra/scalability/-/issues/826).
- Microsoft: [Azure WAF AI workload guide](https://learn.microsoft.com/en-us/azure/well-architected/ai/get-started); [AI workload assessment](https://learn.microsoft.com/en-us/azure/well-architected/ai/assessment); [SaaS workload guide](https://learn.microsoft.com/en-us/azure/well-architected/saas/get-started); [AI agent orchestration patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns).
- Agent vendors: [Anthropic, Building Effective Agents](https://www.anthropic.com/research/building-effective-agents); [OpenAI, A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf); [12-Factor Agents](https://github.com/humanlayer/12-factor-agents).
- Coding-agent mechanisms: [Agent Skills specification](https://agentskills.io/specification); [Claude Code memory and rules](https://code.claude.com/docs/en/memory); [Steering Claude Code blog](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more); [Cursor rules](https://cursor.com/docs/context/rules); [AGENTS.md](https://agents.md/).
- 2025–2026 write-ups: [Packmind context-engineering playbook](https://packmind.com/context-engineering-ai-coding/context-engineering-playbook/); [arXiv 2603.09619](https://arxiv.org/abs/2603.09619); [AGENTS.md advanced patterns](https://codex.danielvaughan.com/2026/03/26/agents-md-advanced-patterns/).

Pages that could not be read directly (content inferred from secondary sources, flagged above): Cortex docs main scorecard page (404; the `.md` mirror was used instead), OpsLevel `/docs/filters` (404; `/docs/checks-and-filters` used), GitLab handbook maturity-model page (nav only; the issue tracker was used), ASVS 5.0 "Using ASVS" chapter (404 on raw GitHub; preface plus two secondary guides used), Backstage tech-insights tree URL (robots; the README blob was used).
