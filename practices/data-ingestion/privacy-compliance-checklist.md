# Privacy and compliance — <<product / corpus>>

Copy to `<repo>/docs/privacy.md` where the full part holds (`personal_data or regulated or multi_tenant`); date it. Principle: `../../principles/16-data-for-ai-products.md` §3.6–3.7. Sources (all in `../../sources/raw/2026-10-01-market-scan-s06-data-audit-cleaning-privacy/`, read 2026-10-01): Chris Gambill (2026-06, `yt-tkFr-4r906Q…`); Chip Huyen, *Building a Generative AI Platform* (2024-07-25, `canon-snapshots/huyen-genai-platform.md`); Presidio README (`canon-snapshots/presidio-readme.md`); EDPB news of 2026-07-08 (`canon-snapshots/edpb-anonymisation-web-scraping-genai.md` — a press release, not the guidelines; re-read the guidelines after the consultation closes on 2026-10-30); Supabase *RAG with Permissions* (`canon-snapshots/supabase-rag-with-permissions.md`); Katharine Jarmul (GOTO 2025 talk, uploaded 2026-01, `yt-lz0L0rRV7RE…`); IBM Technology (2026-09, `yt-kyJ1vd7yEPc…`). Related rows: `../structured-outputs/guardrail-policy.md` G0, G3, G6; `../security-baseline/threat-model-agentic.md` T7, T14, T17, T20; `../memory-and-permissions/permission-model.md` §3.

## 1. The three placements (all three; ingestion is the one that is cheap to prove)

| Placement | Question it answers | Mechanism | Row |
|---|---|---|---|
| **Ingestion** | should this ever be in the index? | `pii_scrub()` before the insert: mask with a placeholder, or quarantine with a reason; "PII filtering must happen before sensitive data gets embedded, indexed, cached, copied" (Gambill) | G0 (Verify 6) |
| **Retrieval** | who may see it? | the tenant and owner predicate in the store — RLS on Postgres, the native partition elsewhere — applied before ranking | G6 (Verify 8) |
| **Output** | did it leak anyway? | redaction on the reply, calibrated against the detector's own warning (§2) | G3 |

## 2. PII classes and recogniser tiers

Classes are "specified by you" (Huyen): list the product's. Tiers follow `../../principles/13-structured-outputs-and-guardrails.md` §3.3 — checksum and regex first, NER second, a classifier or judge last. Presidio combines "Named Entity Recognition, regular expressions, rule based logic and checksum with relevant context in multiple languages" and warns that "there is no guarantee that Presidio will find all sensitive information. Consequently, additional systems and protections should be employed" — copy that sentence into the product's policy; the output net (G3) and the retrieval filter (G6) are those additional systems.

| Class | Detector tier | Policy at ingestion (`PII_POLICY`) | Placeholder | Notes |
|---|---|---|---|---|
| email | regex | mask | `[EMAIL_n]` | reversible |
| phone | regex | mask | `[PHONE_n]` | reversible |
| payment card | checksum (Luhn) + regex | **quarantine** | — | never indexed in any form |
| national id / IBAN | checksum + regex | `<<quarantine>>` | — | per regime |
| person name | NER | `<<mask>>` | `[PERSON_n]` | NER misses; sample the output |
| secret-shaped string (`sk-`, `AKIA`, `ghp_`) | regex | **quarantine** | — | `../security-baseline/` secret scan runs on the corpus too |
| `<<health / special category>>` | classifier | `<<quarantine>>` | — | EDPB: special categories "in principle prohibited" |

Where the test fixture plants one of each class: `<<tests/fixtures/pii/>>` (Verify 6).

## 3. Anonymised or pseudonymised? (EDPB, 2026-07-08)

"Data is anonymous if it does not relate to an identified or identifiable natural person", tested by three criteria — **no record isolation, no linkage, no inference** — under a *contextual approach* (who could realistically re-identify) or a *simplified approach* that gives "greater confidence" at the cost of over-classifying. A reversible placeholder keeps *linkage* through its dictionary: Huyen's "PII reversible dictionary" is **pseudonymisation**, and pseudonymised data is personal data. State it:

```
Stored data is:            <<pseudonymised (reversible placeholders) | anonymised (three criteria met, approach: contextual/simplified) | personal data in clear>>
Reversible mapping lives:  <<secret store under the tenant scope, path/service>>  — never a column beside the embeddings (Verify 9)
Who can unmask:            <<role>>, logged on every unmask
```

**Scraping duties** (when any source is scraped): GDPR applies to "collection, storage, organisation and retrieval"; a lawful basis (legitimate interest, assessed); purpose limitation and transparency; "scraping data only from reliable sources, recording the timestamp, and validating the data"; data minimisation; special categories excluded. Source list and timestamps: `audit-checklist.md` §3; the `ingested_at` field of the envelope is the timestamp.

## 4. Where the owner and tenant tags are written

By the ingestion identity, from the corpus manifest or the job — `tag_owner(doc, ingestion_identity)` — never from the request that triggered a re-index. On Postgres the owner column feeds the RLS policy: `documents.owner_id … default auth.uid()`, `document_sections` with `embedding`, a `select` policy `document_id in (select id from documents where owner_id = (select auth.uid()))`; "semantic search… will continue to respect these RLS policies"; an application `WHERE` is not the control because "RLS is always applied even as new queries and application logic is introduced in the future" (Supabase). Elsewhere: the store's partition plus the mandatory filter of `../memory-and-permissions/permission-model.md` §3. Proof: two tenants, overlapping content, zero cross-tenant hits (Verify 8). "No side door": a user who cannot open a record cannot have a chatbot summarise it (Gambill).

## 5. The erasure path (Gambill; IBM)

"Can you prove that this customer's data was actually deleted…? Did the vector index retain anything? Did [caches] retain anything? Did evaluation data sets retain anything? And what about those logs?" — "test deletion like you're testing your recovery". Data "gets transformed by RAG" (IBM), so the path follows derived copies ("child files… derived from"), not the original form.

| Place | How a subject's data gets there | Erasure step | Proof |
|---|---|---|---|
| Index / vector store | elements with `subject_ids` | delete by `(tenant, subject_id)` | `mentions()` = 0 |
| Answer cache | cached replies that used the elements | invalidate by subject id | 0 |
| Eval datasets | golden cases built from production traces | remove cases tagged with the subject; note the removal in `../evals/eval-policy.md` lineage | 0 |
| Logs and traces | prompts and replies quoting content | redact or delete by subject id within the retention window | 0 |
| Reversible dictionary | placeholders for the subject's values | delete the mapping (the placeholder stays unlinkable) | 0 |
| Memory store | units about the subject | `../memory-and-permissions/memory_store.py` `erase()` | 0 |

Policy window: `<<30 days>>` from the request (`ERASURE_WINDOW_DAYS` in the reference). The proof records `requested_at`, `erased_at` and the deadline for every erasure and fails when `erased_at` is past the deadline (Verify 7). Deletion test: `<<tests/test_erasure.py>>` plants a subject in all six places, runs the path, asserts zero in each **by tag and by content** — a derived copy written without its subject tag is the case the tag proof misses — then checks the window. Reference: `ingestion_pipeline.py` `erase_subject()` → `ErasureRecord`, `mentions()`, `scan_content()`.

## 6. Threats this folder answers (Jarmul; `threat-model-agentic.md`)

"Please never put anything in your prompt that you wouldn't want to write on your public website" (prompt leakage, T11–T12); anything the model can read can be extracted ("the file with everybody's salaries" — T17, hence G0 before the index); "poisoning of… documents that are on your infrastructure" is the likelier vector (T14 — provenance-tagged sources, the audit's authoritative-source table); an unauthenticated public interface will be exploited (T20). Where documents must not leave the environment, a local parser (Docling: "local execution capabilities for sensitive data and air-gapped environments") instead of a vendor API (T7).

## 7. Regimes in scope

| Regime | Applies because | Obligations this file covers | Owner | Review date |
|---|---|---|---|---|
| `<<GDPR>>` | `<<EU data subjects>>` | lawful basis, minimisation, erasure path (§5), anonymisation test (§3) | `<<>>` | `<<>>` |
| `<<EU AI Act / SOC 2 / ISO 27001 / HIPAA>>` | `<<>>` | `<<>>` | `<<>>` | `<<>>` |

The list is the product's; IBM's regime list is column headers, not guidance (digest §3.6).
