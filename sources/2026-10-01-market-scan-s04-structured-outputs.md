---
title: "Market scan — course session 4 'Advanced AI products: structured outputs, guardrails, non-conversational UX': which videos, podcasts and written sources were considered, selected and transcribed"
type: source
status: current
date: 2026-10-01
tags: [market-scan, structured-outputs, guardrails, generative-ui, prompt-templates, s4, lidr-ai-engineering]
sources:
  - sources/raw/2026-10-01-market-scan-s04-structured-outputs/
  - sources/catalog-written-canon.md
  - playbooks/scan-market-for-module.md
supersedes: null
superseded-by: null
---

# Market scan — session 4: advanced AI products (structured outputs, guardrails, non-conversational UX)

**What this file is.** The log of the scan (steps 1–2 of the four-step module cycle): what was searched, what was reused, what was found, what was selected by the authority test, what was discarded and why. The digest (step 3) is a separate entry.

## 1. Context

- **Topic map (LIDR session 4, 2026-11-05).** Non-conversational interfaces and business-oriented UX · structured prompts and dynamic templates · structured data extraction (JSON mode, structured outputs, tool-use extraction, Pydantic/Instructor) · guardrails and response validation.
- **Written canon** (step 1b, registered 2026-10-01 in `sources/catalog-written-canon.md` §Session 4, 15 items): OpenAI and Anthropic structured-outputs docs, Instructor, Claude prompt-template/XML and strengthen-guardrails pages, Guardrails AI, NeMo Guardrails, Llama Guard 4, OpenAI Agents SDK guardrails, Google PAIR guidebook, Microsoft HAX guidelines, Vercel AI SDK generative UI + A2UI, OWASP LLM Top 10, two DeepLearning.AI courses.
- **Reuse (step 1a).** Transcripts from earlier modules that touch this one and are read again for the digest, not re-transcribed: Anthropic *Prompting 101* and *AI prompt engineering: a deep dive* (s1 — prompt structure, templates); Dex Horthy *12-Factor Agents* (s3 — "tools are just structured outputs"); OpenAI *Build Hour: Responses API* (s1 — structured outputs in the Responses API). Grep of `sources/raw/` for "structured output|pydantic|guardrail|json schema": seven earlier transcripts mention them in passing; none is about them.
- **Method.** `streamers/youtube-scraper` run `wlQQabvTB2xTV81kJ` (8 queries × 15, last 12 months, relevance → 120 items, 118 new) + a canon run `vNyojBCmal2f5meDn` without the date filter (8 queries × 8 → 45 items, reference talks older than 12 months) + one targeted run `BLmrvgiWBAtbPLqRL` to find the YouTube version of a podcast episode. `scripts/scan-filter.py`: 118 new, 2 already decided (one s2 IBM video, one s1 discard). Podcasts: the three reference feeds read directly (no Apple search needed); 9 episode titles matched. Transcripts: `johnvc/YoutubeTranscripts` run `dgQxXV6ZJCJ4hpDYZ`, dataset `kaNjIRfrw4p6YZ3Rr`, 13 of 13 with captions, no Whisper. Cost: about US$0.55 for the searches, under US$0.01 for the transcripts.
- **Queries.** "structured outputs LLM JSON schema production" · "Pydantic Instructor structured extraction LLM" · "LLM guardrails output validation production" · "NeMo Guardrails Guardrails AI input output rails" · "generative UI AI product beyond chat interface" · "prompt templates dynamic variables LLM application" · "structured outputs 2026" · "JSON mode vs structured outputs vs tool use extraction"; canon run: "Pydantic is still all you need Jason Liu AI Engineer", "Latent Space Structured Outputs Michelle Pokrass OpenAI", "Latent Space Samuel Colvin Pydantic AI", "BAML structured outputs Boundary talk", "Shreya Rajpal guardrails AI Engineer talk", "AI Engineer World's Fair guardrails production LLM", "AI Engineer generative UI talk 2025", "Instructor structured outputs AI Engineer talk 2025".
- **What the search taught.** The last-12-months market for this module is almost entirely tutorials re-explaining the vendor docs (LangChain prompt templates, "get clean JSON" explainers, NeMo/Guardrails AI crash courses): 146 of 155 new items were discarded, most below the reach floor. The authoritative material is (a) conference talks — AI Engineer 2023–2026, dotAI, Agent Conf, Developer Summit — and (b) the two reference podcasts, and most of it is older than twelve months, which is why the canon run without the date filter was necessary. One real 2026 signal: **Jev**, a small structured-output/classification model from Boundary (the BAML team), with a 444k-view practitioner test in two weeks.

## 2. Selection criteria

The authority test of the pilot (`sources/2026-09-24-market-scan-s12-intro-to-agents.md` §2): primary source > academic or reference conference > recognised practitioner or reference podcast > corporate education > trend signal. Reach floor 5k subscribers / 500 views unless primary. Target met: 13 items, about 8 h 20 min, two podcast episodes, every bullet of the topic map covered by at least two items.

## 3. Selected — transcribed (13)

| Title | Channel | Date | Length | Authority | Serves | Raw file |
|---|---|---|---|---|---|---|
| Pydantic is all you need — Jason Liu | AI Engineer | 2023-11 | 18 m | canon talk | extraction, validation as retry | `yt-yj-wSRJwrrc-aie-jason-liu-pydantic-is-all-you-need.md` |
| Pydantic is STILL all you need — Jason Liu | AI Engineer | 2024-09 | 15 m | canon follow-up | extraction after native structured outputs | `yt-pZ4DIH2BVqg-aie-jason-liu-pydantic-is-still-all-you-need.md` |
| Building AGI with OpenAI's Structured Outputs API — Michelle Pokrass | Latent Space | 2024-09 | 1 h 12 m | reference podcast, primary (OpenAI) | constrained decoding, strict schemas, refusals | `podcast-NjOfH9D8aJo-…pokrass-openai-structured-outputs.md` |
| Agent Engineering with Pydantic + Graphs — Samuel Colvin | Latent Space | 2025-02 | 1 h 02 m | reference podcast, primary (Pydantic) | typed/validated outputs, PydanticAI | `podcast-7wwWRph3Jls-…samuel-colvin-pydantic-ai-graphs.md` |
| Jev Explained: the fast AI model we tried to break on purpose | Boundary | 2026-09 | 43 m | primary (BAML team) | 2026 trend: small structured-output model | `yt-35PSMmDDKP8-boundary-jev-explained.md` |
| Jev — the ultimate classification model? | Sam Witteveen | 2026-09 | 16 m | recognised practitioner | classification/extraction in practice | `yt-X117w2Rark8-sam-witteveen-jev-classification-model.md` |
| $1 AI Guardrails: fine-tuned ModernBERTs — Diego Caravana | AI Engineer | 2026-04 | 44 m | reference conference | guardrail architecture and cost | `yt-YZHPEkfy2kc-aie-diego-caravana-1-dollar-guardrails-modernbert.md` |
| Trust, but Verify — Shreya Rajpal | AI Engineer | 2023-11 | 20 m | canon talk (Guardrails AI) | output validation as a contract | `yt-9-vGxMoUM9Y-aie-shreya-rajpal-trust-but-verify.md` |
| Securing LLMs in production: OWASP Top 10 to guardrails that work — Rohit B. | Developer Summit | 2026-06 | 1 h | conference talk | risk taxonomy → mitigations | `yt-v9wFSDSjb_c-developer-summit-rohit-owasp-to-guardrails.md` |
| Generative UI: specs, patterns and the protocols behind them (MCP Apps, A2UI, AG-UI) | CopilotKit | 2026-01 | 54 m | primary (AG-UI authors) | non-conversational UX | `yt-Z4aSGCs_O5A-copilotkit-generative-ui-specs-patterns-protocols.md` |
| Beyond the chatbot: gen UI and the execution-trust problem — Harshil Agrawal | dotconferences | 2026-09 | 18 m | conference talk | non-conversational UX | `yt-iymZjaNcwc8-dotconf-harshil-agrawal-gen-ui-execution-trust.md` |
| Beyond components: the future of AI UI — Ruben Casas, Agent Conf 2026 | Callstack | 2026-09 | 21 m | conference talk | non-conversational UX | `yt-DLEPGhA4NJQ-callstack-ruben-casas-beyond-components-ai-ui.md` |
| Prompt workshop with Zack Witten (Anthropic) | AI Engineer | 2024 | 1 h 34 m | canon workshop | structured prompts, templates | `yt-hkhDdcM5V94-aie-zack-witten-anthropic-prompt-workshop.md` |

## 4. Considered — not transcribed (every item is in `sources/media-registry.json` with its reason)

- **Parked for other modules (9):** Kent Beck at Prodacity 2026, IBM *Spec-driven development*, OpenAI's *Harness engineering* talk (Ryan Lopopolo, AIE 2026) → s17; Samuel Colvin *Durable agents* and *MCP is all you need*, *Why agentic systems need ontologies* (Frank Coyle, AIE 2026), Latent Space *One year of MCP* → s13; Stanford CME295 *LLM evaluation* lecture → s5; Monty sandboxed interpreter (Latent Space and PyAI Conf) → s14.
- **Discarded, by reason (146 + 2 podcast episodes):** 97 below the reach/authority floor; 28 corporate-education or beginner tutorials re-explaining the vendor docs (Krish Naik, Telusko, NIIT, Scaler, Analytics Vidhya, Padho with Pratyush, DSwithBappy, Sunny Savita…); 9 same-speaker duplicates (Jason Liu, Shreya Rajpal and Samuel Colvin on other podcasts — the higher-authority or more recent version was taken); 4 stack-specific (Spring AI, Java, C#); 4 general prompting explainers; the rest search noise. Podcast episodes discarded: Latent Space *Agent Reasoning Interface* (secondary to the three gen-UI talks) and the 2023 Shreya Rajpal episode (her AIE talk taken instead).
- **Not found with captions:** none; no Whisper spend.

## 5. Still to do

Digest (step 3, `playbooks/ingest-new-source.md`) with the impact table; principle 13 (draft) and a practice for structured outputs + guardrails, created **unrouted** per the routing gate of decision 0004 §6 (module 3's `llm-gateway` has not passed Verify in a real repo yet); move the 13 entries to `digested` → `applied`.

## 6. Raw notes

`sources/raw/2026-10-01-market-scan-s04-structured-outputs/` — 13 transcripts, `youtube-search-results.json` (120), `youtube-search-results-canon.json` (45).
