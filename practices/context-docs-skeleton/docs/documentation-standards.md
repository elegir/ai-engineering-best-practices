# Documentation standards

## 1. Where documentation lives
| Kind | Location | Owner of updates |
|---|---|---|
| Technical context | `docs/*.md` (this folder) | whoever changes the behavior, in the same PR |
| API contract | `docs/api-spec.yml` (generated) | regenerate on any route change |
| Decisions | `<<docs/adr/>>` | author of the decision |
| Runbooks / ops | `<<docs/runbooks/>>` | on-call |
| Product specs / user stories | `<<specs/>>` | product / the SDD tool |
| Code comments | in code | author |

## 2. Which change updates which document
| If you change… | Update |
|---|---|
| a dependency or version | `stack.md` |
| how to run/setup/test | `development-guide.md` |
| a folder, layer, or import rule | `architecture.md` |
| a table, field, relationship | `data-model.md` + regenerate `generated/` |
| an endpoint | `api-spec.yml` (regenerate) + `backend-standards.md` if a convention changed |
| a convention | the matching `*-standards.md` + an ADR if it was a decision |
| the process | `workflow.md` |

The definition of done (`workflow.md`) requires this check before a task is declared finished.

## 3. How to write
- Plain language; explain terms at first use; examples over adjectives.
- Rules carry a **why**. Good/bad examples for anything an agent might get wrong.
- Absolute dates and versions; no "currently".
- Diagrams in Mermaid, in the Markdown, not as images.
- One fact in one place; link elsewhere.

## 4. Code comments
- Comment the *why* and the non-obvious; never narrate the *what*.
- Public functions: a one-line docstring with contract (inputs, outputs, errors).
- TODOs carry an owner and a ticket.

## 5. Freshness
- Each `docs/*.md` may carry a `Last reviewed: YYYY-MM-DD` line at the top; anything older than <<90>> days is reviewed in the next task that touches the area.
