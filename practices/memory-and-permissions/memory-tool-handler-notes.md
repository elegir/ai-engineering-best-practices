# Memory-tool handler notes — what the client must do when the provider's memory tool is used, and the same duties for a home-made store

Read before adding Anthropic's memory tool to a product; implement as `memory_tool.py` (or the stack's equivalent) against the same store as `memory_store.py` if the tool is used; otherwise read it for the duties and delete. Principle: `../../principles/15-memory-external-context-and-permissions.md` §3.3. Source: the Anthropic memory tool page as read on 2026-10-01 (`../../sources/raw/2026-10-01-market-scan-s05-context-memory-permissions-evals/canon-snapshots/anthropic-memory-tool.md`) — digest §3.6. Vendor facts are dated; re-read the page on adoption day.

## What the tool is (2026-10-01)

A **client-side** tool: `{"type": "memory_20250818", "name": "memory"}` in the request is the whole configuration. The model issues commands — `view`, `create`, `str_replace`, `insert`, `delete`, `rename` — against paths under `/memories`, and **your application executes them against storage you control** (the page's words); that the provider therefore holds no copy of the memory content is this KB's reading of that sentence, not a statement on the page — confirm against the data-retention terms before relying on it. The API adds an instruction automatically ("ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE… ASSUME INTERRUPTION: your context window might be reset at any moment"), so the model reads memory first and writes as it goes. SDK helpers exist for Python, TypeScript, C#, Java; Go and Ruby run the loop by hand; PHP wraps a handler in the generic runnable-tool helper. The interface is files; the substrate is yours (`memory-design.md` §6).

## The handler's duties (the page's security section, restated as a checklist)

| Duty | Rule | In `memory_store.py` terms |
|---|---|---|
| **Path validation** | canonicalise every path; reject anything outside `/memories`; refuse `../` and URL-encoded traversal (`%2e%2e`) — the page's rules; *reject symlinks* is this KB's addition for a file-backed store | `validate_namespace()` — the scope is the identity's namespace, traversal shapes refused (assertion 6) |
| **Per-identity root** | `/memories` is **per user or tenant** in a multi-user product: the handler maps it to `<store>/<owner>/…`; the model never sees another owner's root | `store.for_owner(identity)` as the first predicate |
| **Sensitive-data stripping** | "Claude usually refuses… for stronger guarantees, add validation": run the include/exclude check on every `create` / `str_replace` / `insert` payload before writing | `_passes_exclusions()` on the written text (assertion 5) |
| **Size caps** | cap file size and the output of `view` so a memory file cannot flood the window | `MAX_READ_CHARS`, `k` (assertion 7) |
| **Expiry** | expire unused files; expiry is lifecycle, not guaranteed deletion — a separate erasure path where law requires | decay score; `forget()` vs `erase()` (assertion 4) |
| **Audit** | every command logged with identity, path, size, outcome | the unit's trail; the application's audit log for erasures |
| **Concurrency** | two sessions of one user writing the same file: last-writer-wins or a lock — decide | the store's responsibility (Alake's ACID point, without the one-database preference) |

## Pairing with compaction (s2)

The page states the relation this KB adopts: "compaction keeps the active context small without client-side bookkeeping, and memory preserves the information that must survive summarization". Memory is the **offload** operation of `../../principles/11-runtime-context-management.md` §3.2 in its provider-side form; compaction is **reduce**. Use both; never rely on a summary to carry a fact that matters — write it to memory before the trigger (`../context-management/compaction-policy.md`'s `must_preserve` list is the same idea for the window side).

## The multisession pattern (software work across sessions)

For an agent that works on a task over several sessions: an **initializer** session writes a progress log and a feature checklist to memory; every later session **reads them first and updates them last**; a feature is complete "only after end-to-end verification". This is the provider-side form of `../session-state/` (`PROGRESS.json`, `/start-session`, `/end-session`): same contract, the file lives in the memory store instead of the repo.

## When not to use the provider's tool

- The product is user-facing and memory should be quiet and consolidated — a background extract → consolidate pass (`memory_store.py`) suits better than the model deciding when to write (digest §5: a tool-triggered write suits agents on their own tasks; a background pass suits user-facing memory). The handler duties above still apply to whatever writes.
- The product runs on a provider without the tool — the duties are the contract; implement them against your store.
