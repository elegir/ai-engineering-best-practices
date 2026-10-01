---
title: "Catalogue — written canon per course session: the docs, papers, articles and courses of maximum authority, registered so none is read twice"
type: source
status: current
date: 2026-09-30
tags: [catalogue, written-sources, canon, registry]
sources:
  - sources/media-registry.json
  - playbooks/scan-market-for-module.md
supersedes: null
superseded-by: null
---

# Written canon per session

**What this file is.** Step 1 of the four-step module cycle (`playbooks/scan-market-for-module.md`): the written sources of maximum authority for each course session, found by web research (first pass 2026-09-24, Claude Project doc `curso-fuentes-sesiones-*.md`) and registered in `sources/media-registry.json` with `type: written` so that a later scan never re-examines them. Statuses: `catalogued` (listed, not yet read in full), `cited` (used in a digest or principle — the reason says where), `discarded`. Check a URL with `python3 scripts/written-filter.py <url>` before reading it. Sessions are added here as each module is scanned; the rest of the 2026-09-24 catalogue stays in the Project doc until then.


## Cross-cutting (every session)

| Source | Author / org | Date | Status | Where cited / note | URL |
|---|---|---|---|---|---|
| 12-Factor Agents | Dex Horthy (HumanLayer) | 2025 | cited | author's talk digested in s2 (Pragmatic Engineer); repo not yet read — read for s3 | https://github.com/humanlayer/12-factor-agents |
| Building effective agents | Anthropic | 2024-12-19 | cited | cited in principles/21 §6 (s12) | https://www.anthropic.com/engineering/building-effective-agents |
| Emerging Patterns in Building GenAI Products | Martin Fowler & Bharani Subramaniam | 2025 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://martinfowler.com/articles/gen-ai-patterns/ |
| Patterns for Building LLM-based Systems & Products | Eugene Yan | 2023-07 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://eugeneyan.com/writing/llm-patterns/ |
| What We Learned from a Year of Building with LLMs (Parts I–III) | Applied LLMs (Yan, Bischof, Frye, Husain, Liu, Shankar) | 2024-05 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://www.oreilly.com/radar/what-we-learned-from-a-year-of-building-with-llms-part-i/ |

## Session 1 — LLMs and environment setup

| Source | Author / org | Date | Status | Where cited / note | URL |
|---|---|---|---|---|---|
| Building LLM applications for production | Chip Huyen | 2023-04-11 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://huyenchip.com/2023/04/11/llm-engineering.html |
| Building with the Claude API (course) | Anthropic Academy | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://anthropic.skilljar.com/claude-with-the-anthropic-api |
| ChatGPT Prompt Engineering for Developers (course) | DeepLearning.AI × OpenAI | 2023 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://www.deeplearning.ai/courses/chatgpt-prompt-eng |
| Context windows (Claude Platform Docs) | Anthropic | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://platform.claude.com/docs/en/build-with-claude/context-windows |
| Get started with Claude / llms.txt index | Anthropic | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://platform.claude.com/llms.txt |
| Long context (Gemini API docs) | Google | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://ai.google.dev/gemini-api/docs/long-context |
| Prompt Engineering (Lil'Log) | Lilian Weng | 2023-03-15 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/ |
| Prompt engineering guide (OpenAI API docs) | OpenAI | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://developers.openai.com/api/docs/guides/prompt-engineering |
| Prompting best practices (Claude 4.x) | Anthropic | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices |

## Session 2 — CAG: context, parameters, costs

| Source | Author / org | Date | Status | Where cited / note | URL |
|---|---|---|---|---|---|
| Compaction (Claude Platform Docs) | Anthropic | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://platform.claude.com/docs/en/build-with-claude/compaction |
| Context Engineering for Agents | Lance Martin (LangChain) | 2025-06-23 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://rlancemartin.github.io/2025/06/23/context_engineering/ |
| Context Rot | Chroma Research | 2025-07 | cited | cited in principles/11 §3.1 | https://www.trychroma.com/research/context-rot |
| Context caching (Gemini API docs) | Google | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://ai.google.dev/gemini-api/docs/caching |
| Context engineering | Simon Willison | 2025-06-27 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://simonwillison.net/2025/jun/27/context-engineering/ |
| Don't Do RAG: When Cache-Augmented Generation is All You Need | Chan et al. (arXiv 2412.15605) | 2024-12 | cited | cited in principles/11 §3.4 | https://arxiv.org/abs/2412.15605 |
| Effective context engineering for AI agents | Anthropic | 2025-09-29 | cited | cited in principles/11 §6 and the s2 digest | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| Lost in the Middle | Liu et al. (arXiv 2307.03172) | 2023-07 | cited | cited in principles/10 §3.4 and 11 §3.1 | https://arxiv.org/abs/2307.03172 |
| Prompt caching (Claude Platform Docs) | Anthropic | 2026 | cited | cited in practices/llm-api-calls and context-management READMEs (re-check before promoting to current) | https://platform.claude.com/docs/en/build-with-claude/prompt-caching |
| Prompt caching (OpenAI API docs) | OpenAI | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://developers.openai.com/api/docs/guides/prompt-caching |
| Prompt caching vs semantic caching | Redis | 2025 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://redis.io/blog/prompt-caching-vs-semantic-caching/ |

## Session 3 — Wrappers and layered architecture

| Source | Author / org | Date | Status | Where cited / note | URL |
|---|---|---|---|---|---|
| 12-Factor Agents talk — Dex Horthy, AI Engineer 2025 | AI Engineer | 2025-06 | candidate | listed in the written-canon catalogue (Project doc); to be taken by the s3 scan | https://www.youtube.com/watch?v=8kMaTybvDUw |
| AI SDK (Vercel) docs | Vercel | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://ai-sdk.dev/docs/introduction |
| Build a basic LLM chat app (Streamlit docs) | Streamlit | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps |
| Creating a Chatbot Fast (gr.ChatInterface) | Gradio | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://gradio.app/guides/creating-a-chatbot-fast |
| Fast Prototyping of GenAI Apps with Streamlit (course) | DeepLearning.AI × Snowflake | 2025 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://www.deeplearning.ai/courses/fast-prototyping-of-genai-apps-with-streamlit |
| GPT Semantic Cache | Regmi & Pun (arXiv 2411.05276) | 2024-11 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://arxiv.org/abs/2411.05276 |
| Langfuse observability docs | Langfuse | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://langfuse.com/docs/observability/overview |
| LiteLLM Router: load balancing, fallbacks & reliability | BerriAI | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://docs.litellm.ai/docs/routing |
| LiteLLM proxy reliability (fallbacks/failover) | BerriAI | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://docs.litellm.ai/docs/proxy/reliability |
| OpenRouter provider routing | OpenRouter | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://openrouter.ai/docs/guides/routing/provider-selection |
| OpenRouter: reliability & failover explained | OpenRouter | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://openrouter.ai/blog/insights/reliability-failover/ |
| OpenTelemetry GenAI semantic conventions (spans) | OpenTelemetry | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/ |
| Productionizing LLM Gateways — Kanish Manuja (Twilio), AI Engineer World's Fair 2026 | AI Engineer | 2026 | candidate | listed in the written-canon catalogue (Project doc); to be taken by the s3 scan | https://www.youtube.com/watch?v=zrZ1amZBSPw |
| Reducing latency (Claude Platform Docs) | Anthropic | 2025 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency |
| Semantic caching for LLMs (RedisVL) | Redis | 2025 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://redis.io/docs/latest/develop/use-cases/semantic-cache/ |
| Streaming messages (Claude Platform Docs) | Anthropic | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://platform.claude.com/docs/en/build-with-claude/streaming |
