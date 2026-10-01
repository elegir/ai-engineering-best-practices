# Implement a practice from the knowledge base — the one prompt for any stack

Use as `/implement-practice <practice-name>` (Claude Code command) or paste. It refers to the practice's sections by heading and restates nothing, so it cannot drift when the practice changes (decision 0005 §9). The agent runs it **inside the target repo**, after `playbooks/which-practices-apply.md` (or the bootstrap) listed the practice as applying.

---

You are implementing the practice `<<PRACTICE>>` from the AI-engineering knowledge base at `<<KB_PATH>>` in **this** repository. Read `<<KB_PATH>>/practices/<<PRACTICE>>/README.md` once, fully, before touching anything. Then work in this order and do not skip a step.

**1. The contract.** The section `## Verify` is the definition of done. Every numbered assertion must hold at the end; nothing else counts as "done" — not "it looks right", not "the file is copied". Copy the assertions into your plan as a checklist. For each, note its observer: `script` means you will run a command and show its exit code; `agent` means you will demonstrate it in this session and quote what happened; `Martin` means you will prepare exactly what he has to read, in one screen, and stop for him.

**2. Where this repo's stack changes the mechanism.** Read `## Stack-sensitive points`. If this repo's runtime is one of the cases named there (request-scoped process, secrets in a non-`.env` file, URLs in the database, an audit tool without a severity threshold…), the mechanism in the reference does **not** apply as written; design the equivalent that still satisfies the assertion, and say which point you applied. If `stack-notes/<this stack>.md` exists in the practice folder, follow it: it names the package family to use and the names that differ from the reference. Do not research package families on your own when the note exists; when it does not exist, say so in the field report — that absence is a finding.

**3. The reference.** `## Reference implementation` names the file(s) and which parts are *idiom, not required*. The order of authority is fixed: **the assertions beat the repo's framework beat the reference.** Concretely: an assertion marked `framework: beats` wins even if this repo's library does it differently (one retry owner, usage logged, no secrets in traces); an assertion marked `bends` adapts to the repo's idiom (exceptions instead of result objects, the framework's own test runner); and the reference is consulted for *shape*, never copied into a framework that already provides the shape. Do not invent a new framework, wrapper or abstraction if the repo already has one that satisfies the assertion.

**4. Files.** `## Files in this folder` and `## Adapt` say what to copy and what to replace. Every `<<PLACEHOLDER>>` is replaced or the file is not copied. Each file goes where the table says, under this repo's conventions; the KB is never edited from here (decision 0001).

**5. Prove it.** Run every `script` assertion and paste the command and its result. Demonstrate every `agent` assertion and quote it. For every assertion, also perform its **negative** once (break the thing on purpose, observe the failure, restore) — an assertion whose negative did not fail is not satisfied. Then stop and hand the `Martin` assertions to him in one screen.

**6. The field report.** Before you end, write `<<KB_PATH>>/templates/field-report.md` filled in, as a message (you do not write into the KB): the practice, this repo and commit, the stack, each assertion with pass/fail and the evidence, the stack-sensitive points you applied, **tokens spent on this adoption, wall-clock minutes, and the number of wrong API or framework calls the Verify caught** (zero is a valid number; "not counted" is not). Martin passes the report to the KB, which turns it into a variant through `<<KB_PATH>>/playbooks/adopt-variant.md`.

Rules that hold throughout: investigate before you implement and show the plan first; one practice per session; never weaken a sensor (test, hook, lint) to make an assertion pass; if an assertion cannot hold in this repo for a technical reason, say the reason in the report instead of marking it done.

---

**Adapt:** `<<PRACTICE>>`, `<<KB_PATH>>` (the guide's path on this machine; `scripts/kb-sync.sh --pull` has been run). Nothing else; the prompt reads the practice's headings, which `scripts/kb-check.sh` keeps stable.
