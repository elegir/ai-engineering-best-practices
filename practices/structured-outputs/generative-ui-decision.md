# Generative UI decision — static, declarative or open-ended, per screen; the renderer is an allow-list; model-written code is untrusted

Copy to `<repo>/docs/ui-generation.md` when the model decides what the interface shows (a dashboard, an admin tool, a report builder, a non-chat workflow). Principle: `../../principles/13-structured-outputs-and-guardrails.md` §3.5. Sources: CopilotKit, *Generative UI: specs, patterns and the protocols behind them* (2026-01); Ruben Casas, Postman, *Beyond components* (Agent Conf 2026, 2026-09); Harshil Agrawal, Cloudflare, *Beyond the chatbot: gen UI and the execution trust problem* (dotJS 2026, 2026-09); Michelle Pokrass on recursive schemas (2024-09) — digest `../../sources/2026-10-01-s04-structured-outputs-digest.md` §3.5. Protocol detail (AG-UI, A2UI, MCP Apps) is parked for session 13; code-sandboxing depth for session 14.

## Why this is a structured-outputs question

Chat is "not the most efficient or the final form" of the LLM computer (Casas); a chat agent over an admin dashboard produced "text blurb" that became unreadable as conversations grew (Agrawal, in production). In every alternative the model **emits data that a renderer maps to components** — a tool call, a JSON tree, a state object — never free text the page inserts. "Every UI is a nested tree that has children" (Pokrass): generative UI is a recursive structured output with a renderer at the end, and everything in `schema-design-rules.md` applies to the spec the model emits.

## The three tiers — choose per screen

| Tier | The model emits | The front end does | Pros | Cons | Use it for |
|---|---|---|---|---|---|
| **Static** | a tool call or a typed state with known arguments | maps the tool name to a **developer-built component** (CopilotKit's `useRenderToolCall`; a registered component) | pixel-perfect; designers in control; simple mental model | **coupling**: the tool's name and arguments are an API contract between back end and front end; "the codebase is going to grow linearly with your use cases" (CopilotKit) | the two or three well-trodden paths of the product (an order card, an approval panel) |
| **Declarative** | a **JSON description** of the screen over a constrained **component catalogue** (Google's A2UI, launched 2025-12, pre-1.0 in 2026-01; json-render; the precedent is Netflix's server-driven, per-user home page — Casas) | a renderer walks the tree and instantiates catalogue components; "the structure of the content is non-deterministic but the actual rendering of it is deterministic" | design system and accessibility kept; "you fully control what each of these individual components look like… it's just the structure that changes"; "probably the best balance" (Casas) | constrained by the catalogue (a calculator display is hard); structure varies run to run | **the default** for business UIs — dashboards, admin tools, back-office automation (the KB's opinion for Martin's shapes) |
| **Open-ended** | HTML or code | renders it in an **iframe** or runs it in an isolate (MCP Apps — the renamed MCP-UI; ChatGPT apps) | lowest coupling; "render anything" | unpredictable ("looks slightly different every single time"); hard to style; **expensive** to regenerate; off the design system; users "like to know where things are"; a **security** surface (XSS) | consume-and-discard visualisations, inside the sandbox below; never the product's main screens |

Decision per screen, written in the spec: `screen · tier · catalogue or component list · who owns the contract · sandbox (if open-ended)`.

## The renderer is an allow-list

Whatever the tier, the renderer is a `switch` over **known component types**, with **no default branch that renders**. Validate the spec against its schema on the server *and* in the browser; an unknown type — including a smuggled `html` or `script` node — is simply not rendered: "the last defense point" (Agrawal). Never `dangerouslySetInnerHTML` (or the equivalent) on model output. The spec's schema is a closed object with every key required (`schema-design-rules.md`); the catalogue is the vocabulary the model may use, and growing it is a reviewed change, not a prompt edit.

## Model-written code is untrusted code — the three questions (Agrawal's production rules)

When the open-ended tier is chosen, or when the model writes a function at request time to compute what to show (Agrawal's dashboard: the model writes JavaScript that fetches through a typed tool and returns a *description* of the UI — "there is no React code written by the model, there is no JSX, there is no HTML"), answer three questions before shipping:

| Question | Control | Negative (what must be impossible) |
|---|---|---|
| **What can the code access?** | only the tools handed to it; each tool enforces its input schema and throws on anything outside it; the model never writes SQL or reaches a database directly | a query string from the model reaching the database; a tool accepting arguments its schema does not name |
| **What can it do while running?** | it runs **outside the app** in an isolated runtime (Agrawal: a V8 isolate / dynamic worker — "spinning up a container is just futile" for one JavaScript function; a container or a sandboxed interpreter in other stacks) with **outbound network denied by default** (`globalOutbound: null`) or an explicit allow-list of URLs, and a **CPU-time limit** | a `fetch` to an attacker's domain succeeding; code that runs in the application's process or with its credentials; an infinite loop that holds a worker |
| **What comes back?** | the return value is validated against the UI schema on the server and again in the browser; the renderer allow-list above; size caps | an unknown component type rendered; raw HTML or a script inserted; a payload larger than the screen could ever need |

"Whenever you have generated code by an LLM, treat it as an untrusted code… run the model-written code outside your app" (Agrawal). This is the UI-side instance of `../security-baseline/` and of the bounded-tools rule in `../../principles/21-agent-design-and-tools.md` §3.4; how to build the sandbox in each stack is session-14 material.

## Typed events and typed state, both ways

The UI consumes **typed events** from the layer (`../../principles/12-llm-gateway-layer.md` §3.3, §3.6) and, where the user and the agent work on the same artifact, **typed state in both directions**: state snapshots and deltas flow from agent to UI *and* a human edit becomes agent context; a human-in-the-loop interrupt is a first-class event, not a text message (CopilotKit's AG-UI demonstrations; Casas's "collaboration on a shared artifact" as the more valuable near-term pattern — both vendors' opinions, recorded as such). Streaming a declarative spec means streaming **partial typed objects** (Liu's *partial* mode) and rendering fields as they validate — never splicing text deltas into the page.

## Checklist

- [ ] tier chosen and written per screen; declarative unless a reason is recorded
- [ ] the spec schema is closed, all-required, versioned; the catalogue is the allow-list; no default render branch
- [ ] server-side *and* client-side validation of what the model returned
- [ ] no `dangerouslySetInnerHTML` / `innerHTML` / `v-html` on model output anywhere (grep)
- [ ] if code is generated: isolated runtime, outbound network denied or allow-listed, CPU limit, typed tools only — and a test that proves a `fetch` to an unknown host fails
- [ ] the UI holds no model logic (`../llm-gateway/`); swapping the UI touches no prompt
