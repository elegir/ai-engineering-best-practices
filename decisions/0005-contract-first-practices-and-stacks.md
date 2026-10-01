---
title: "0005 — A practice is a contract (Verify), stack-sensitive points, one reference implementation and an implementation prompt; the KB keeps no speculative per-stack ports, writes short stack-notes instead, authors variants bottom-up from real repos, and ships the security guard as one fail-closed artefact"
type: decision
status: accepted
date: 2026-09-30
tags: [decision, stacks, verify, contract, variants, hooks, laravel, php, typescript, python, promotion]
sources:
  - sources/2026-09-30-stack-debate.md
  - sources/2026-09-30-day-one-debate.md
  - decisions/0004-day-one-for-blank-and-existing-repos.md
supersedes: null
superseded-by: null
---

# 0005 — Contract-first practices and stacks

## Context

Martin's products run on Python/FastAPI (AI SDR, Content Central), PHP/WordPress (sites), PHP/Laravel (a multi-tenant app) and some TypeScript. Decision 0004 §3 (2026-09-30) said the bootstrap for a blank repo ships only files that passed Verify somewhere, and therefore required "hooks rewritten in Python" and "a TypeScript port of the day-0 LLM client" before any bundle promises a TypeScript stack. The same evening Martin asked whether the KB should keep copyable files per technology at all: best practices do not change by stack, and a KB that ports every file to every language never scales. A devil's-advocate debate (`sources/2026-09-30-stack-debate.md`) tested the resulting proposal — contract + prompt + one Python reference — and found it right about invariants and wrong about four things: the Verify sections are not contracts yet; the agent cannot reliably research package families and runtime pitfalls alone; a Python hook on a machine without Python fails *open*; and saving a consumer's version back needs a reviewer and a version link.

## Decision

1. **Invariants do not change by stack; mechanisms sometimes do, and the KB names where.** Every practice README has a `## Stack-sensitive points` section: the places where the *mechanism* depends on the runtime model (request-scoped PHP-FPM vs a long-lived process; secrets in `wp-config.php` or a cached config file vs `.env`; URLs embedded in a database; what a dependency audit can and cannot fail on). Two to five bullets, written once, by the KB.

2. **The Verify section is the contract.** It is a numbered list of stack-neutral assertions, each in the shape `N. <assertion> — observer: script | agent | Martin — negative: <what breaks it>`, and each tagged **beats the framework** or **bends to it** where the repo's existing framework could conflict. Stack-specific commands live only in an "Example commands (Python)" sub-list below the assertions. `scripts/kb-check.sh` fails on a Verify line that does not parse. The invariants that today live in skeleton docstrings (one client module, variable content last, one retry owner, usage logged, no LLM opinion guarding an irreversible action…) move into the contract.

3. **One reference implementation per practice, in Python**, under `## Reference implementation`, labelled with `reference-status: untested | field-tested | reference` in the practice frontmatter. Today every reference is `untested`; it becomes `field-tested` when a real repo passes the rewritten Verify with it (first expected: AI SDR, `llm-api-calls`). Python idioms in the reference (a `Result` dataclass instead of exceptions, for instance) are marked "idiom, not required". The prompt's order of authority is **invariants > the repo's own framework > the reference**.

4. **No speculative ports.** The KB writes no PHP or TypeScript code until a real repo of that stack consumes a practice. This **supersedes two sentences of 0004 §3**: "hooks are rewritten in Python" stands in the stronger form of §6 below; "a TypeScript port of the day-0 LLM client exists before any bundle promises a TypeScript stack" is replaced by: **TypeScript is not a promised stack** until a field-tested TS variant exists, and the bundle generator marks it "no reference yet". The day-one goal is amended accordingly: for a stack with no field-tested variant, the KB gives a blank repo the working-style files, the guard, and for each capability practice the contract, the stack-notes and the implementation prompt — not capability *files*.

5. **Stack-notes instead of ports.** For each stack Martin actually runs, a practice may carry `stack-notes/<stack>.md` of at most fifteen lines and no code: the package family to use with its source URL and "check the current version at adoption" (no version pins — they are stale on day one), the three or four names that differ from the reference, and the two runtime pitfalls. `stack-notes/python.md` and `stack-notes/php-laravel.md` are written now where they matter (`llm-api-calls`, `llm-gateway`, `hooks-and-guards`, `verification`, `security-baseline`); `php-wordpress` where it already exists (`hooks-and-guards/variants/`, migrated into this format); TypeScript when a consumer appears. The existing `variants/*.md` files are the first stack-notes.

6. **The security guard is one artefact, fail-closed.** `practices/hooks-and-guards/` ships a single Python guard reading its stack commands from `hooks.json` (standard library only — no `tomllib`), wired in `settings.json` as `python3 .claude/hooks/guard.py <event> || exit 2`, so a missing interpreter **blocks** instead of letting the action through (Claude Code treats any exit code other than 2 as non-blocking). The guard has `--selftest`; the entry-file startup routine runs it so a dead guard is reported every session; the destructive-command patterns are duplicated in Claude Code's native `permissions.deny` as the first layer.

7. **Variants are authored by the KB, tested in the consumer.** When a repo of a new stack adopts a practice: the agent follows the implementation prompt in that repo; the field report (`templates/field-report.md`) records tokens spent, wall-clock minutes and wrong API calls caught by Verify; the KB then writes the variant into `practices/<name>/variants/<stack>/` through `playbooks/adopt-variant.md` with frontmatter `status: field-tested`, `verified-against: <practice last-reviewed date>`, `field-report: <path>`. A variant becomes `reference` after a clean-context review against the contract's negative cases within thirty days of the field report (not "after a second consumer" — for a solo founder the second consumer rarely comes). `kb-check.sh` flags a variant whose `verified-against` is older than its practice's `last-reviewed`. The router shows a variant's status to the adopting agent.

8. **Cost rule.** When two adoptions in the same stack each spend more than **100,000 tokens** on translating one practice (field-report field), the KB ships that stack's variant proactively for every routed practice. The number is revisable with a change-log line.

9. **The implementation prompt** is one template, `practices/prompt-library/implement-practice.md`, that refers to a practice's sections by heading (`## Verify`, `## Stack-sensitive points`, `## Reference implementation`, `stack-notes/`) and restates nothing, so it cannot drift; it carries the two obligations no heading holds — the tie-break rule and the field report. The headings are a schema `kb-check.sh` enforces on every routed practice.

10. **Experiment before module 4 is routed.** Two arms on the existing Laravel repo with `llm-api-calls`, fresh context each: (a) prompt + contract alone; (b) prompt + contract + `stack-notes/php-laravel.md`. Tokens, minutes and wrong API calls caught by Verify are recorded for both. If (a) is not materially worse than (b), §5 is reduced to "stack-sensitive points only" with a change-log line here; if (b) is not materially better than a hand-written port would have cost, §4 is revisited.

## Consequences

- The KB's per-stack work is bounded: a `## Stack-sensitive points` section and, where it matters, fifteen lines of notes — not N copies of every file.
- The Verify rewrite is the real work this decision creates, and it benefits every consumer regardless of stack: an agent can now tell when it is done.
- 0004 §3 is partly superseded (two sentences; see §4); 0004 §8's acceptance test must name the stacks of shapes A and B — both Python until a field-tested variant exists elsewhere, and the test says so.
- Decision 0001 (the KB writes nothing into target repos) stands: the prompt and the contract are read; the repo writes its own files.
- Order of execution: `sources/2026-09-30-stack-debate.md` §4, items 1–10.
