---
title: "Method log — where the four-step module cycle failed or wobbled, and what was changed so it does not happen again"
type: source
status: current
date: 2026-10-01
tags: [method-log, process, market-scan, digest, review, lessons]
sources:
  - playbooks/scan-market-for-module.md
  - playbooks/ingest-new-source.md
  - decisions/0002-market-scan-protocol-and-media-registry.md
supersedes: null
superseded-by: null
---

# Method log

One row per failure or wobble of the module cycle (written canon → scan → digest → principle + practice → review → publish), with the date, the module where it showed, what went wrong, and the fix — a rule, a script, a playbook line. Martin asked for this on 2026-10-01 ("vayamos anotando si hay algo de la metodología que falla para que la arreglemos"). Entries are appended; nothing is deleted. The `Fixed in` column names the file that carries the rule now, so a future reader can check it is still there.

| Date | Module | What failed | Fix | Fixed in |
|---|---|---|---|---|
| 2026-09-28 | AI SDR test | Two copies of the KB diverged (four commits unpushed for three weeks); the consuming agent worked from a stale guide | `kb-sync.sh` as the first command of every session; `kb-publish.sh` refuses to publish when ahead | `AGENTS.md`, `scripts/kb-sync.sh` |
| 2026-09-30 | s3 | US$4 of Whisper on a podcast episode whose RSS title promised engineering content and whose body was an investor conversation | Read the show notes before paying for Whisper; search YouTube for the captioned version first | `playbooks/scan-market-for-module.md` step 5 |
| 2026-09-30 | s3 | A source useful to two modules was treated as "already used" and nearly not re-read | Registry = pay once, never use once; step 1a reuse-first; `modules[]` list per entry | `playbooks/scan-market-for-module.md` step 1a |
| 2026-09-30 | s3 | Written sources were never registered, so a doc could be read twice by two modules | Written canon registered with `type: written`; `scripts/written-filter.py` on every URL | step 1b; `scripts/written-filter.py` |
| 2026-10-01 | s4 | The scan log attributed Jev to the wrong company (Boundary, which only ships a client); the error came from reading titles, not transcripts, at selection time | Selection text is provisional until the digest; a scan log may receive an appended, dated *Correction* paragraph; digests and other source bodies are never edited | `playbooks/scan-market-for-module.md` step 7 |
| 2026-10-01 | s4 | The digest agent read the canon pages through a summarising fetch and stated two vendor facts wrongly (`pattern` unsupported; "doubles state space" attributed to unions); a third misattribution (the "smart if-statement" to Boundary) survived into the principle | The clean-context review before publishing is **mandatory**, not optional, for every module; it spot-checks at least twelve attributed claims against the raw transcripts and re-reads the vendor pages directly; vendor limits are never promoted from a summarised fetch | `playbooks/ingest-new-source.md` step 2c (review) |
| 2026-10-01 | s4 | The Python reference `structured_call.py` had dead code: the SDK's `parse()` validated eagerly, so the re-ask branch it documented could never run; `--demo` passed because it never exercised the branches | A reference implementation is executed against a stubbed client for **every branch its docstring names** before publishing, and the stub run is recorded in the practice's change log | `playbooks/ingest-new-source.md` step 3d |
| 2026-10-01 | s4 | The new principle came out at 33.6 KB against an 18–28 KB aim; the house style (every claim attributed) and a seven-subsection outline pull in opposite directions | Outline the principle with a byte budget per subsection; prose that repeats a practice file becomes a pointer | `templates/principle.md` note |
| 2026-10-01 | s4 | WebFetch permission prompts timed out in unattended sessions; agents fell back to direct HTTP, which the workspace rules discourage | Canon pages that matter are fetched by the main session before delegating (or their text is saved under `sources/raw/` as a written-source snapshot); a sub-agent never works around a blocked fetch | this log; `playbooks/scan-market-for-module.md` step 1b |
| 2026-10-01 | s4 | A new practice could not be published unrouted because `kb-check` demanded a README row | `routed: false` frontmatter key; kb-check [4] and `check-practices.py` honour it | `CONVENTIONS.md` §4b, `practices/_template/README.md` |
| 2026-10-01 | bootstrap A/B | The first two real runs found 48 defects in the KB that no review had caught (walking-skeleton rule missing, template failing its own Verify, script bugs) | Field reports are the KB's main sensor; every module's practice waits for one (routing gate); the acceptance test stays in the plan after every structural change | `decisions/0004-day-one-for-blank-and-existing-repos.md` §6, §8; `practices/adoptions.md` |

## How to add a row

When a step of the cycle fails, add the row **in the same publish** as the fix, and make sure the fix is a sentence in a playbook, a line in a template or a check in a script — not only a row here.
