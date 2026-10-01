# Data audit — <<corpus>>

Copy to `<repo>/docs/data-audit.md`; one copy per corpus; date it; regenerate the report section on every parser, source or policy change (Verify 1). Principle: `../../principles/16-data-for-ai-products.md` §3.2. Sources: Andrew Ng, Data+AI Summit (2022-07, `yt-avoijDORAlc…`); Chris Gambill, *How to design a data pipeline that's LLM-ready* (2026-06, `yt-tkFr-4r906Q…`); Reducto (2026-01, `yt-ybzR4LBY0Lo…`; 2026-09, `yt-0I07YAuF8xA…`) — all in `../../sources/raw/2026-10-01-market-scan-s06-data-audit-cleaning-privacy/`. The report itself is produced by `ingestion_pipeline.py --audit`; this file records what the report cannot know: who owns what, which source is authoritative, which contracts and gates apply.

## 1. Inventory (from the report, `ingestion_pipeline.py --audit <<CORPUS_PATH>> --report audit.json`)

```
Corpus: <<name>>                          Report date: <<>>        Parser version in the report: <<>>
Documents: <<n>>   by type: <<.pdf n, .docx n, .html n, .csv n, …>>
Duplicates (content hash): <<n groups>>  → decision: <<keep one, tombstone the rest / keep all because different owners>>
Empty pages: <<n>>   garbled pages (text density < <<0.55>>): <<n>>  → decision: <<re-scan / OCR / drop>>
PII hits by class: <<email n, phone n, card n, secret n, …>>       → full part: privacy-compliance-checklist.md
Date coverage: <<earliest>> → <<latest>>, undated: <<n>>           → freshness rule in §4
Sources with no owner: <<n>>                                       → §2 before anything is indexed
```

Gambill's landing-zone minimum, restated as the four questions the report answers: can we identify the source? detect obvious schema breakage? quarantine records that are malformed? tag sensitivity and region? A corpus that cannot answer all four is not ready for an index.

## 2. Authoritative source per business concept (Gambill)

"Which sources are authoritative for which business concepts" is decided before ingestion, because "computers are very good at making bad decisions repeatable". One row per concept the product answers about.

| Concept | Authoritative source | Other sources that mention it | Rule when they disagree |
|---|---|---|---|
| `<<refund window>>` | `<<policies/refunds-v3.pdf>>` | `<<support macros, old FAQ>>` | `<<authoritative wins; the others are indexed with sensitivity "internal" and a lower rank, or not at all>>` |

## 3. Owner and sensitivity per source (the envelope's inputs)

Written here or in the corpus manifest (`manifest.json` beside the files: owner, tenant, region, date, sensitivity per path); the ingestion job reads it — never a request (Verify 2, 8).

| Source (path or feed) | Owner (team or tenant) | Sensitivity (`public` / `internal` / `confidential` / `personal`) | Region | Freshness need | Date field |
|---|---|---|---|---|---|
| `<<policies/>>` | `<<ops>>` | `<<internal>>` | `<<eu>>` | `<<daily>>` | `<<document date in the header>>` |

## 4. Data contracts (Gambill)

A contract "is not just the column exists… a real contract includes shape, meaning, ownership, freshness, compatibility rules, and what happens when the contract breaks". One per source feed; the parser version is part of the shape.

| Source | Shape (format, schema, parser version) | Meaning (what a field means, units) | Ownership (who fixes it) | Freshness ("what business decision gets worse if the data is 5 minutes old?") | Compatibility (what may change without notice) | On break |
|---|---|---|---|---|---|---|
| `<<crm export>>` | `<<CSV, 14 columns, parser v>>` | `<<amount in EUR cents>>` | `<<ops>>` | `<<hourly; a stale price misquotes>>` | `<<new columns allowed; renamed columns break>>` | `<<quarantine the batch, alert owner, keep last good>>` |

## 5. Gates (Gambill: four in the data plane, one for AI)

| Gate | Checks | Fails → |
|---|---|---|
| Source contract | the feed matches §4's shape; identifiable source; timestamp present | quarantine the batch |
| Schema and meaning | fields parse; units and enums as declared | quarantine the records |
| Quality | the report's thresholds: duplicates, empty/garbled pages, density, date coverage | re-parse or drop; record the decision |
| Publish | lineage written (source id, parser version, ingested-at) | nothing is indexed without it |
| **AI approval** | "gold data is not automatically AI approved data": may this set be embedded? retrieved by a model? acted on by an agent? does it contain PII (→ `privacy-compliance-checklist.md`)? how fresh must it be? what lineage must reach the answer? | the set stays out of the index; the decision is dated here |

AI approval decision for `<<corpus>>`: <<embed yes / retrieve yes / act no — because …>> (date <<>>).

## 6. The label book (Ng) — when the corpus is labelled or routed by type

Inconsistent labels mean "I didn't write clear enough labeling instructions"; the fix is a labelling instruction document the team edits, with examples of each class and of the ambiguous cases, plus **agreement-based labeling** (several labelers on the same items to surface disagreements) and **slicing** to the subset that fails. For ingestion the labels are the document classes of Reducto's *classify and split* (invoice, contract, form, correspondence…) and the routing per class. Location: `<<docs/label-book.md>>`; last agreement check: <<date, n items, agreement %>>. The same rule governs eval labels in `../evals/error-analysis-log.md`.

## 7. Parser evaluation (Reducto; Verify 4)

Never "five documents". Sample `<<≥ 1,000>>` pages across every type and source in §1 (the long tail included: scans, forms, merged-cell tables), run each candidate parser, compare automatically against a reference (field-level for extraction, element-level for structure), and keep the result here: parser `<<name, version>>`, date `<<>>`, sample size `<<>>`, failure classes found `<<>>`. Production sample: `<<n pages / day>>` re-parsed and compared, reviewed in `../evals/error-analysis-log.md`.

## 8. Re-audit triggers (Ng: cleaning "is a core part of the iterative process")

Regenerate the report and re-run §5 when: the parser version changes; a source is added, removed or changes shape; a policy in `privacy-compliance-checklist.md` changes; the error-analysis log attributes a failure class to an ingestion cause. The report's `parser_version` not matching the parser in use is Verify 1's negative — build the check into CI.
