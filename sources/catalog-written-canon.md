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
| Build a basic LLM chat app (Streamlit docs) | Streamlit | 2026 | cited | cited in principles/12 §3.6 (canon for the UI bullet; no video selected) | https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps |
| Creating a Chatbot Fast (gr.ChatInterface) | Gradio | 2026 | cited | cited in principles/12 §3.6 | https://gradio.app/guides/creating-a-chatbot-fast |
| Fast Prototyping of GenAI Apps with Streamlit (course) | DeepLearning.AI × Snowflake | 2025 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://www.deeplearning.ai/courses/fast-prototyping-of-genai-apps-with-streamlit |
| GPT Semantic Cache | Regmi & Pun (arXiv 2411.05276) | 2024-11 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://arxiv.org/abs/2411.05276 |
| Langfuse observability docs | Langfuse | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://langfuse.com/docs/observability/overview |
| LiteLLM Router: load balancing, fallbacks & reliability | BerriAI | 2026 | cited | cited in principles/12 §3.2 and practices/llm-gateway/gateway_config.yaml (read 2026-09-30) | https://docs.litellm.ai/docs/routing |
| LiteLLM proxy reliability (fallbacks/failover) | BerriAI | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://docs.litellm.ai/docs/proxy/reliability |
| OpenRouter provider routing | OpenRouter | 2026 | cited | cited in practices/llm-gateway/README.md (re-read before promoting to current) | https://openrouter.ai/docs/guides/routing/provider-selection |
| OpenRouter: reliability & failover explained | OpenRouter | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://openrouter.ai/blog/insights/reliability-failover/ |
| OpenTelemetry GenAI semantic conventions (spans) | OpenTelemetry | 2026 | cited | page moved to the semantic-conventions-genai repo (status Development); cited in principles/12 §3.4 and practi | https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/ |
| Productionizing LLM Gateways — Kanish Manuja (Twilio), AI Engineer World's Fair 2026 | AI Engineer | 2026 | candidate | listed in the written-canon catalogue (Project doc); to be taken by the s3 scan | https://www.youtube.com/watch?v=zrZ1amZBSPw |
| Reducing latency (Claude Platform Docs) | Anthropic | 2025 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency |
| Semantic caching for LLMs (RedisVL) | Redis | 2025 | cited | cited in principles/12 §3.5 and practices/llm-gateway/semantic-cache-decision.md | https://redis.io/docs/latest/develop/use-cases/semantic-cache/ |
| Streaming messages (Claude Platform Docs) | Anthropic | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; read w | https://platform.claude.com/docs/en/build-with-claude/streaming |

## Session 4 — Advanced AI products: structured outputs, guardrails, non-conversational UX

| Source | Author / org | Date | Status | Where cited / note | URL |
|---|---|---|---|---|---|
| Structured model outputs (OpenAI API docs) + launch post | OpenAI | 2026 | cited | cited in principles/13 §3.1 and practices/structured-outputs/schema-design-rules.md (read 2026-10-01 through the fetch tool's summary — limits omitted; re-read directly before promotion) | https://developers.openai.com/api/docs/guides/structured-outputs |
| Structured outputs (Claude Platform Docs) + announcement | Anthropic | 2025-11 | cited | cited in principles/13 §3.1, principles/11 §3.3 and practices/structured-outputs/schema-design-rules.md, structured_call.py (read 2026-10-01) | https://platform.claude.com/docs/en/build-with-claude/structured-outputs |
| Instructor — structured outputs for LLMs (docs, repo, 'Pydantic is all you need' keynote write-up) | Jason Liu / 567 Labs | 2023–2026 | cited | cited in principles/13 §3.2 and practices/structured-outputs/validation-and-reask.md (front page read 2026-10-01) | https://python.useinstructor.com/ |
| Use prompt templates and variables · Use XML tags (Claude docs) | Anthropic | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables |
| Strengthen guardrails: reduce hallucinations · increase consistency · mitigate jailbreaks (Claude docs) | Anthropic | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations |
| Guardrails AI (repo + validator hub docs) | Guardrails AI (Shreya Rajpal) | 2023–2026 | cited | cited in principles/13 §3.3 and practices/structured-outputs/guardrail-policy.md, guardrail-tiers.md (README read 2026-10-01) | https://github.com/guardrails-ai/guardrails |
| NeMo Guardrails (overview, Colang guide, repo) | NVIDIA | 2023–2026 | cited | cited in principles/13 §3.3, principles/12 §3.3 and practices/structured-outputs/guardrail-policy.md (overview read 2026-10-01) | https://docs.nvidia.com/nemo/guardrails/about-nemo-guardrails-library/overview |
| Llama Guard 4 model card + Llama Protections | Meta | 2025-04 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://developer.meta.com/ai/docs/model-cards-and-prompt-formats/llama-guard-4/ |
| Guardrails (OpenAI Agents SDK) + openai-guardrails-python + guardrails & approvals guide | OpenAI | 2026 | cited | cited in principles/13 §3.3, principles/12 §3.3 and practices/structured-outputs/guardrail-policy.md, llm-gateway/routing-policy.md (read 2026-10-01) | https://openai.github.io/openai-agents-python/guardrails/ |
| People + AI Guidebook (principles & patterns) | Google PAIR | 2019–2025 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://pair.withgoogle.com/guidebook/ |
| Guidelines for Human-AI Interaction (HAX Toolkit) | Microsoft Research | 2019–2025 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/ |
| Generative User Interfaces (AI SDK UI) · A2UI v0.9 | Vercel · Google Developers | 2024–2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://ai-sdk.dev/docs/ai-sdk-ui/generative-user-interfaces |
| OWASP Top 10 for LLM Applications (2025) / GenAI LLM Top 10 (2026) | OWASP GenAI Security Project | 2024-11 / 2026 | cited | cited in principles/13 §3.3 and practices/security-baseline/threat-model-agentic.md rows T11–T20 (landing page read 2026-10-01: the 2025 list; check for a 2026 edition) | https://genai.owasp.org/llm-top-10/ |
| Pydantic for LLM Workflows (course) | DeepLearning.AI | 2025 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://www.deeplearning.ai/courses/pydantic-for-llm-workflows |
| Safe and Reliable AI via Guardrails (course) | DeepLearning.AI × Guardrails AI | 2024 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://www.deeplearning.ai/courses/safe-and-reliable-ai-via-guardrails |

## Session 5 — Advanced features: external context, memory, permissions, evals

| Source | Author / org | Date | Status | Where cited / note | URL |
|---|---|---|---|---|---|
| Files API · PDF support (Claude Platform Docs) | Anthropic | 2026 | cited | cited in principles/15 §3.4, practices/memory-and-permissions/external-context-notes.md and threat-model T21 (s5; snapshot canon-snapshots/anthropic-files-api.md, read 2026-10-01) | https://platform.claude.com/docs/en/build-with-claude/files |
| Web search tool · Web fetch tool · MCP connector · tool-use overview (Claude Platform Docs) | Anthropic | 2026 | cited | cited in principles/15 §3.4, principles/11 §3.2, external-context-notes.md and the transport table (s5; snapshot canon-snapshots/anthropic-web-search-tool.md, read 2026-10-01) | https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/web-search-tool |
| Introducing the Model Context Protocol | Anthropic | 2024-11-25 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://www.anthropic.com/news/model-context-protocol |
| Memory tool (Claude Platform Docs) | Anthropic | 2026 | cited | cited in principles/15 §3.3, principles/11 §3.2 and practices/memory-and-permissions/memory-tool-handler-notes.md (s5; snapshot canon-snapshots/anthropic-memory-tool.md, read 2026-10-01) | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool |
| Memory overview (LangChain docs) · LangMem conceptual guide | LangChain | 2026 | cited | cited in principles/15 §3.1 and practices/memory-and-permissions/memory-design.md (s5; snapshot canon-snapshots/langchain-memory-concepts.md, read 2026-10-01; LangMem guide stays for the validation pass) | https://docs.langchain.com/oss/python/concepts/memory |
| Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory (arXiv 2504.19413) | Mem0 (Chhikara et al.) | 2025-04 | cited | cited in principles/15 §3.2 and practices/memory-and-permissions/memory_store.py (s5; abstract only — snapshot canon-snapshots/mem0-arxiv-abstract.md, read 2026-10-01; mechanism carried, LOCOMO numbers not) | https://arxiv.org/abs/2504.19413 |
| MemGPT: Towards LLMs as Operating Systems (arXiv 2310.08560) | Packer et al. (UC Berkeley) | 2023-10 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://arxiv.org/abs/2310.08560 |
| RAG with Access Control | Pinecone | 2026-01-08 | cited | cited in principles/15 §3.5, practices/memory-and-permissions/permission-model.md and guardrail-policy.md G6 (s5; snapshot canon-snapshots/pinecone-rag-access-control.md, read 2026-10-01; written by AuthZed's Sohan Maheshwar, 2026-01-08) | https://www.pinecone.io/learn/rag-access-control/ |
| OWASP Top 10 for LLM Applications 2025 — LLM06 Excessive Agency, LLM02 Sensitive Information Disclosure | OWASP GenAI Security Project | 2024-11 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/ |
| Guardrails and human review (OpenAI Agents guide: guardrails & approvals) | OpenAI | 2026 | cited | cited in principles/15 §3.5, practices/verification/dry-run-and-approval.md 2b and guardrail-policy.md G4 (s5; snapshot canon-snapshots/openai-agents-guardrails-approvals.md, read 2026-10-01) | https://developers.openai.com/api/docs/guides/agents/guardrails-approvals |
| Your AI Product Needs Evals | Hamel Husain | 2024-03-29 | cited | cited in principles/14 §3.1–3.2 and practices/evals/ (s5; snapshot canon-snapshots/hamel-your-ai-product-needs-evals.md, read 2026-10-01) | https://hamel.dev/blog/posts/evals/index.html |
| Demystifying evals for AI agents | Anthropic (Engineering) | 2026-01 | cited | cited in principles/14 §3.2–3.5, practices/evals/eval-policy.md and eval_harness.py (s5; snapshot canon-snapshots/anthropic-demystifying-evals-for-ai-agents.md, read 2026-10-01) | https://anthropic.com/engineering/demystifying-evals-for-ai-agents |
| Define your success criteria · Create strong empirical evaluations (Claude Platform Docs) | Anthropic | 2026 | cited | cited in principles/14 §3.2 (the Likert dissent) and §3.3 (s5; snapshot canon-snapshots/anthropic-develop-tests.md, read 2026-10-01) | https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests |
| Evaluating the Effectiveness of LLM-Evaluators · An LLM-as-Judge Won't Save the Product | Eugene Yan | 2024-08 / 2025 | cited | cited in principles/14 §3.1–3.2 (both posts: llm-evaluators 2024-08 and eval-process 2025-04) and the glossary (s5; snapshots canon-snapshots/eugeneyan-llm-evaluators.md, eugeneyan-eval-process.md, read 2026-10-01) | https://eugeneyan.com/writing/llm-evaluators/ |
| Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (arXiv 2306.05685) | Zheng et al. (LMSYS) | 2023-06 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://arxiv.org/abs/2306.05685 |
| promptfoo docs (intro, CI/CD, red team) | promptfoo | 2026 | cited | cited in principles/14 §3.5 and practices/evals/stack-notes/python.md (s5; snapshot canon-snapshots/promptfoo-intro.md, read 2026-10-01) | https://www.promptfoo.dev/docs/intro/ |
| DeepEval docs (getting started, metrics, G-Eval) | Confident AI | 2026 | cited | cited in principles/14 §3.5, practices/evals/eval-policy.md and stack-notes/python.md (s5; snapshot canon-snapshots/deepeval-getting-started.md, read 2026-10-01; GEval threshold and JevEval dated) | https://deepeval.com/docs/getting-started |
| AI Evals For Engineers & PMs (course) | Maven — Hamel Husain & Shreya Shankar | 2025 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://maven.com/parlance-labs/evals |
| Evaluating AI Agents (course) | DeepLearning.AI × Arize | 2025 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://www.deeplearning.ai/courses/evaluating-ai-agents |
| LLMs as Operating Systems: Agent Memory (course) | DeepLearning.AI × Letta | 2024 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://www.deeplearning.ai/courses/llms-as-operating-systems-agent-memory |
| Introduction to Model Context Protocol · MCP: Advanced Topics (courses) | Anthropic Academy | 2026 | catalogued | written canon for the module, catalogued 2026-09-24 in the Project doc curso-fuentes-sesiones-01-05.md; registered 2026-10-01; read when the module is digested | https://anthropic.skilljar.com/introduction-to-model-context-protocol |
