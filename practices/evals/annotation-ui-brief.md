# Brief — build the review and annotation app for <<product>>

Run this as a prompt to the coding agent (Claude Code or equivalent) once the first traces are exported. The app is the tool that makes "looking at the data" cheap; it is built in hours, not bought (Husain 2024: "build my own data viewing & labeling tool… in less than a day"; Nurture Boss "within a few hours"; DoorDash 2026-08: ops teams "vibe-code their own annotation UIs" over "very stable APIs"). Principle: `../../principles/14-evals-and-error-analysis.md` §3.4–3.5. The division of labour is Shankar's (2026-07) and is the point of this brief: **the agent builds the tooling, maintains the taxonomy and proposes instances; the human does the analysis and owns every label.**

---

You are building a local review app for the traces of <<product>>. Investigation before implementation: read the export first, propose the screens in one message, wait for approval, then build.

**Input.** A JSONL (or CSV) export at `<<evals/export/traces.jsonl>>`, one trace per line with at least: `trace_id`, `timestamp`, `input`, `output`, `messages[]` (role, content, tool calls and results in order), `metadata` (model, prompt version, user segment). The export comes from `<<Langfuse / LangSmith / the traces table>>`; do not change its shape — read it.

**Screens.**

1. **Trace viewer.** The full transcript on one screen, tool calls and results inline and collapsible, metadata in a side panel, keyboard next/previous. Everything the reviewer needs on one screen; no clicking into sub-pages (Husain's "gather all the information I need onto one screen").
2. **In-situ note.** A single text box per trace for the open-coding note (the most upstream error, one sentence) and a one-click "no issue"; saved to `<<evals/annotations.jsonl>>` with `trace_id`, `note`, `reviewer`, `timestamp`. No rubric, no scales, no dropdown of failure modes on the first pass — the categories do not exist yet.
3. **Filters and sampling.** Filter by metadata (date range, model, prompt version, segment, has-tool-call, length); **random sample of n**; and, once clusters exist, **sample per cluster** so each failure mode gets fresh traces.
4. **Cluster map.** After ≥ 20 notes: a view of the current axial codes (from `<<evals/error-analysis.md>>` §2) with counts, the "none of the above" bucket, and the notes under each. The taxonomy file is the source of truth; the app reads and writes it only through the explicit "propose" action below.
5. **Progress.** Traces reviewed / total, notes per day, saturation hint (new codes per 20 traces).
6. **Label export.** For each failure mode that has a judge: export `{trace_id, output, label: pass|fail}` to `<<evals/labels/<failure-mode>.jsonl>>` with a training/held-out split column, so `eval_harness.py --calibrate` can run.

**What the agent does, and does not do, with the taxonomy.**

- You may **cluster** the notes into candidate axial codes and show them; you may **propose** that a trace is an instance of an *existing* failure mode and surface it to the reviewer for a yes/no.
- You **never** add a failure mode to the taxonomy yourself, never relabel a trace the reviewer labelled, and never score traces. "I don't tell the agent to find me entirely new examples of failure modes… I don't love the experience of just trying to validate the agent's taste" (Shankar).
- Every proposal is persisted (`evals/proposals.jsonl`) so there is a **reusable intermediate**: definitions, examples, counts — the three mistakes Shankar names are "evaluate the app" with no artifact, reviewing each trace once, and one uniform accuracy bar for everything.

**Constraints.** Local, single user, no auth, no network except reading the export; <<Streamlit / Gradio / a small FastAPI + HTML>>; starts with one command; data files are the interface so another tool can replace the app. Keep it under <<500>> lines; this is a tool for looking, not a product.

**Done when.** Martin has reviewed twenty traces through it in one sitting without leaving the screen, the notes file has twenty rows, and `eval-policy.md` §6 names the app.
