---
title: "Debate — contract first, one reference, no per-stack ports: a clean-context devil's advocate attacks the proposal that practices are stack-agnostic contracts (Verify) plus an implementation prompt plus one Python reference; two rounds; what survived"
type: source
status: current
date: 2026-09-30
tags: [debate, devil-advocate, stacks, verify, contract, hooks, variants, laravel, php, typescript, governance]
sources:
  - sources/2026-09-30-day-one-debate.md
  - decisions/0004-day-one-for-blank-and-existing-repos.md
  - practices/README.md
supersedes: null
superseded-by: null
---

# Debate — do best practices change by stack, and who writes the translation?

## 1. Context

After decision 0004 was published (2026-09-30, `f82d193`), Martin asked whether the KB should keep copyable files per technology at all. His products run on Python/FastAPI, PHP/WordPress, PHP/Laravel (a multi-tenant app) and some TypeScript. His position: "best practices of vibe coding do not change by stack; the KB should give the *prompt* to implement the practice and the consuming repo researches its own stack; otherwise we write everything once per technology." The author agreed and proposed:

> Each practice = (1) **the contract**: its Verify section, stack-agnostic; (2) **an implementation prompt** — "implement in this repo, with its stack, something that satisfies the contract; look at the reference; do not invent a framework the repo does not have"; (3) **one reference implementation in Python** as an example, not a requirement. The first Laravel consumer produces its version from the prompt, passes Verify, and that version is saved back as a tested variant. **Exception:** security hooks ship as one tested Python file for all repos, because they run around the agent, not inside the product. Stack defaults shrink to: reference in Python; other stacks born from a real repo; hooks one file for all.

**Method.** A devil's-advocate agent with clean context read the repo at `f82d193` (every practice README's Verify section, the hooks, the skeletons, decisions 0001/0004, the first debate) and attacked the proposal in two rounds. Round 1: 15 attacks with evidence and alternatives. Round 2: the author's concede / partly / defend, and the advocate's rebuttals plus an ordered must-change list. Condensed below; the exchange is in this session's transcript.

## 2. Round 1 — attacks that mattered (condensed)

| # | Attack | Evidence |
|---|---|---|
| 1 | **Verify is not a contract today.** Of 14 Verify sections only four (`verification`, `dry-run-and-approval.md`, `hooks-and-guards` 1–4, `security-baseline` core 1) are observable assertions an agent in any language can judge. The rest are Python/Node commands (`grep … src/ \| grep import`, `npx lefthook run`, `pip-audit`), Claude-Code slash commands (`/ask-expert`, `/context`), or "a reviewer can read and approve". `_template/README.md` defines Verify in one line with no shape | `practices/*/README.md` §Verify |
| 2 | **"Research your own stack" is the failure the KB exists to prevent.** `llm_call_skeleton.py` depends on vendor field names (`cache_control`, `max_retries=0`, `budget_tokens < max_tokens`, `cache_read_input_tokens`); in PHP the agent chooses among several package families with different retry behaviour; three Laravel repos pick three; a wrapper that retries internally reintroduces the two-retry-owners anti-pattern that `llm-gateway` forbids | `llm-api-calls/llm_call_skeleton.py`, `llm-gateway/routing-policy.md` |
| 3 | **Cost moves from one reviewed place to N unreviewed places and nobody measures it** | debate 1 round 2: "nobody measures what a bootstrap costs" |
| 4 | **Save-back has no reviewer and no gate**; a wrong-but-passing variant becomes canon; Martin does not review PHP | `templates/field-report.md`, `practices/adoptions.md` both "to be created" |
| 5 | **The Python-hooks exception fails open.** Claude Code treats a hook exit code other than 2 as non-blocking: `python3: command not found` (exit 127) → the edit proceeds. On a Windows machine of a PHP developer Python is often absent. And it is not "one file": `stop-gate.sh` carries `TEST_CMD`, `post-edit-quality.sh` a `case` per extension, `settings.json` stack-specific allow entries | `hooks-and-guards/dot-claude/` |
| 6 | **A bootstrap cannot be made of prompts**; 0004 §3 says it ships only Verify-passed files; a day-one Laravel fintech would receive six prompts and no code | `decisions/0004-day-one-for-blank-and-existing-repos.md` §3, §8 |
| 7 | **The premise is false for some practices**: the *mechanism* changes with the runtime model — PHP-FPM is request-scoped (no in-process cooldown; retries in queued jobs), Laravel `config:cache` copies secrets into `bootstrap/cache/`, WordPress embeds URLs in the DB (worktrees do not apply), `composer audit` has no severity threshold | `llm-gateway/streaming-pipeline.md`, `protect-files.sh`, `worktrees/`, `variants/php-wordpress.md` |
| 8 | **The Python reference biases every port**: `Result` dataclass returning errors instead of raising is a Python idiom; Laravel's idiom is exceptions; the prompt says both "look at the reference" and "use the repo's framework" with no tie-break | `llm_call_skeleton.py` |
| 9 | **The proposal silently overturns 0004 §3** (accepted the same day: Python hooks refusing placeholders *and* a TypeScript day-0 client) with zero new evidence | AGENTS.md "respect accepted decisions" |
| 10 | **Cost-shifting dressed as philosophy**: it reverses Martin's 2026-09-08 instruction that practices carry copyable files (principle 09 change log; decision 0001) | `principles/09-knowledge-base-design.md`, `decisions/0001-knowledge-base-structure.md` |
| 11 | **No evidence either way**; the proposal replaces one untested link with four (prompt → research → translation → Verify → save-back) | `token-savings/measurement-log.md`: "a number, not an impression" |
| 12 | **Hand-written prompts drift** from the README after ingests (`llm-api-calls` edited twice in three days); kb-check cannot see it | change logs |
| 13 | **No rule for when the repo's framework violates the contract** (a wrapper with internal retries; a plugin storing the key in the options table) | — |
| 14 | **Saved variants carry no relation to the contract version** | practices have `last-reviewed`; variants would have nothing |
| 15 | **Per-stack files already exist** (`hooks-and-guards/variants/{node,python,php-wordpress}.md`); "no per-stack files" either deletes them (forbidden) or pretends | `hooks-and-guards/variants/` |

**What the advocate would not change:** one reference instead of N speculative ports; variants born bottom-up from a real repo that passed Verify; hooks shipped as one tested artefact around the agent; contract before code *in principle*; "do not invent a framework the repo does not have"; a smaller stack-defaults decision.

## 3. Round 2 — responses and rebuttals

| # | Author | Advocate's rebuttal (kept) |
|---|---|---|
| 1 | Concede: rewrite all 14 Verify sections as numbered stack-neutral assertions with observer and negative case; Python commands into an "Example commands (Python)" sub-list; kb-check lint | A keyword blocklist misses `ruff`, `vendor/bin`, `/context`…; make the lint **structural**: every Verify line outside the examples must parse as `N. <assertion> — observer: script\|agent\|Martin — negative: <what breaks it>` |
| 2 | Partly: write "Stack-sensitive points" per practice now; defer `stack-notes/php-laravel.md` until a consumer | **Incoherent with 11**: the Laravel consumer exists tonight; deferring the notes means the experiment measures the failure mode (agent researching package families alone), not the method. "Stale on day one" argues against *pinning versions*, not against notes. Write `stack-notes/php-laravel.md` now: package family + source URL + "check current version at adoption" + differing field names + pitfalls. TS deferral is fine (no consumer named) |
| 3 | Concede: tokens / minutes / wrong API calls caught by Verify mandatory in the field report; two adoptions in a stack over N tokens → ship the variant proactively | "N undefined never fires" — put a number in the decision |
| 4+14 | Concede: variant frontmatter `status: field-tested`, `verified-against`, `field-report`; promotion to `reference` on second consumer or clean-context review; kb-check staleness check | "Second consumer" repeats the bundles error for a solo founder; promotion = **clean-context review against the negative cases within 30 days**; a variant that stays `field-tested` is acceptable but must be visible in router output |
| 5 | Concede: one Python guard + config file; wired `\|\| exit 2`; `--selftest`; destructive commands also in native `permissions.deny` | `hooks.toml` needs `tomllib` (Python ≥ 3.11) — another fail-open path; use **`hooks.json`**; run `--selftest` from the entry-file startup routine so a dead guard is reported every session |
| 6 | Partly: working-style set is files; capability practices on a non-Python stack = contract + prompt + stack-sensitive points; bundle marked "no reference yet" | Honest only if (a) the day-one goal wording says that for a non-Python stack the KB gives no capability *files* on day one, (b) 0004 §8 names the stacks of shapes A and B, (c) "no reference yet" reaches the **agent** at adoption time (`applies.py --explain`, `ROUTER.md`), not only kb-check at publish time |
| 7 | Concede: "Stack-sensitive points" section; premise restated as "invariants don't change; mechanisms sometimes do; the KB names where" | — |
| 8 | Concede: invariants to the contract; Python idioms demoted; prompt order invariants > repo framework > reference | — |
| 9 | Concede governance (decision 0005 supersedes two sentences of 0004 §3); defend content: the TS client is written when the first TS consumer appears | Accepted on two conditions: **the Python reference is labelled `reference-status: untested`** until the AI SDR adoption passes the rewritten Verify (the same standard indicts it), and TypeScript is removed from the list of *promised* stacks until a field-tested variant exists |
| 10 | Concede: the KB authors the variant through ingest; the consumer repo is the test bench | Impact-table verdicts do not describe accepting code; name the procedure (`playbooks/adopt-variant.md`) |
| 11 | Concede: experiment on the existing Laravel repo before module 4 is routed | One arm proves nothing; **two arms**, fresh context each: prompt + contract alone, then prompt + contract + stack-notes; record tokens, minutes, wrong API calls caught; the numbers decide item 2 for later stacks |
| 12 | Partly: one prompt template in `prompt-library/` that refers to sections **by heading** instead of generating | Fine only if the headings are a **schema kb-check enforces** (`## Solves`, `## Applies when`, `## Does not apply when`, `## Files`, `## Reference implementation`, `## Stack-sensitive points`, `## Adapt`, `## Verify`, `## Sources`, `## Change log`); "the reference is `## Files`" is wrong today — Files lists five files of which one is code |
| 13 | Concede: each contract assertion tagged *beats the framework* or *bends to it* | — |
| 15 | Concede: `variants/*.md` become the stack-notes format | — |

## 4. Agreed — what changes, in order (all accepted by the author after round 2)

1. **Rewrite Verify for all 14 routed practices** as numbered stack-neutral assertions with observer and negative case; Python commands into an "Example commands (Python)" sub-list; `_template/README.md` carries the section schema including `## Reference implementation` and `## Stack-sensitive points`.
2. **kb-check**: structural Verify lint; section-schema check per routed practice; `verified-against` staleness check on variants; "no reference yet" for a stack without a field-tested variant, surfaced by `applies.py --explain` / `ROUTER.md`, not only by kb-check.
3. **Hooks**: one Python guard + `hooks.json`; wired `python3 … || exit 2` (fail closed); `--selftest` in Verify and in the entry-file startup routine; destructive commands duplicated in native `permissions.deny`.
4. **Contracts**: invariants promoted from skeleton docstrings into Verify, each tagged beats/bends; Python idioms demoted to "idiom, not required"; `llm_call_skeleton.py` tagged `reference-status: untested`.
5. **Stack-sensitive points** in every practice; **`stack-notes/python.md` and `stack-notes/php-laravel.md`** now (no version pins; package family with source URL, differing names, pitfalls); `hooks-and-guards/variants/*.md` migrated into that format; TS when a consumer appears.
6. **Implementation prompt** as one template in `prompt-library/`, by heading, carrying the tie-break rule and the field-report obligation.
7. **Decision 0005**: supersedes the two sentences of 0004 §3; amends the day-one goal for non-Python stacks; TypeScript removed from promised defaults until a variant exists; N for the cost rule fixed; the two-arm experiment named as reverting evidence.
8. **Field-report template** with mandatory cost fields; `playbooks/adopt-variant.md`; `practices/adoptions.md`.
9. **Two-arm Laravel experiment** on `llm-api-calls`; results ingested.
10. Only then: module 4 routed; the 0004 §8 acceptance test with its stacks named.

## 5. Opinions recorded as opinions

The author's view that deferring the TypeScript day-0 client is right because "a file nobody runs is zero evidence" was accepted, but the advocate turned it on the Python reference: the same standard makes the reference an untested draft, and it is now labelled as such. Martin's premise — practices do not change by stack — was kept as a statement about *invariants* and rejected as a statement about *mechanisms*; the "Stack-sensitive points" section is where the two meet. Both are judgment calls recorded here so a later reader knows they were weighed.
