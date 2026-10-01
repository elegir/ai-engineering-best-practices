---
title: "Practice — <name>"
type: practice
status: draft            # draft | current | superseded
date: YYYY-MM-DD
last-reviewed: YYYY-MM-DD
tags: []
kind: working-style | capability   # working-style = any repo an agent works in; capability = depends on what the product does
applies-when: "always | <one line using only words from practices/facts.md>"
# full-when: "<facts that attach the practice's conditional part>"   # optional (see security-baseline)
when: day-0            # day-0 | first-user | at-scale — when in a product's life it is installed (decision 0004 §5)
reference-status: untested   # untested | field-tested | reference — decision 0005 §3; only a field report moves it
# routed: false              # add while the practice must stay unrouted (decision 0004 §6): no row in practices/README.md, absent from ROUTER.md; kb-check reads it. Remove the key when the routing gate is met.
principle: principles/NN-topic.md
sources:
  - sources/YYYY-MM-DD-slug.md
supersedes: null
superseded-by: null
---

# <Practice name>

## Solves
One paragraph: the concrete problem in a repo that this fixes, and how you notice it (symptoms).

## Applies when
- …

## Does not apply when
- …

## Files in this folder
| File | Copy to | Purpose |
|---|---|---|
| `…` | `<repo>/…` | … |

## Reference implementation
Which file(s) above are the reference (Python), and which parts of them are *idiom, not required* (decision 0005 §3). Other stacks: `stack-notes/<stack>.md` (≤ 15 lines, no code, no version pins) and, once a real repo passed Verify, `variants/<stack>/`.

## Stack-sensitive points
Two to five bullets: where the *mechanism* (not the syntax) depends on the runtime model — request-scoped vs long-lived process, where secrets live, what the audit tool can fail on, URLs embedded in a database… Write "none" if there are none.

## Adapt
What must change per repo: placeholders `<<LIKE_THIS>>`, stack variants, things to delete.

## Verify
The contract. Every line is a numbered stack-neutral assertion in this exact shape (kb-check fails otherwise):

`N. <assertion> — observer: script | agent | Martin — negative: <what must make it fail>` and, where the repo's framework could conflict, ` — framework: beats | bends`.

Stack-specific commands go only in a final paragraph starting with **Example commands (…)**.

## Sources
Links to `sources/` and URLs.

## Section schema
These headings, in this order, are mandatory on every routed practice and checked by `scripts/kb-check.sh`: Solves · Applies when · Does not apply when · Files in this folder · Reference implementation · Stack-sensitive points · Adapt · Verify · Sources · Change log. (Delete this section from a real practice.)

## Change log
- YYYY-MM-DD — created.
