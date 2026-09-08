# Development guide

<!-- Rule: everything here must work by copy-pasting the commands, on a clean machine, with no tribal knowledge. If a step needs a human decision, say what to decide. -->

## 1. Prerequisites
- <<OS notes (Windows: use Git Bash / WSL?)>>
- <<Runtime + version manager>>
- <<Docker Desktop>> (for the database and services)
- Access: <<what credentials a developer needs and where to request them — never the values>>

## 2. First-time setup (from zero)
```bash
git clone <<REPO_URL>>
cd <<REPO_DIR>>
cp .env.example .env            # then fill the values listed in §7
<<install command>>
docker compose up -d db          # database only
<<migration command>>
<<seed command>>                 # loads the sample dataset described in §4
```
Expected result: `<<health check URL or command>>` returns `<<expected output>>`.

## 3. Everyday commands
| Task | Command |
|---|---|
| Start everything | `<<docker compose up>>` |
| Start only backend + frontend (DB already running) | `<<…>>` |
| Reset the database | `<<…>>` |
| Run unit tests | `<<…>>` |
| Run integration tests | `<<…>>` |
| Run e2e tests | `<<…>>` |
| Lint + format | `<<…>>` |
| Type check | `<<…>>` |
| Build | `<<…>>` |

## 4. Seed data
What the seed contains (users, roles, sample records) and the credentials of the seeded test accounts (test-only). Agents use these for e2e.

## 5. Running in a git worktree
Each worktree needs its own port and database name so parallel sessions don't collide.
```bash
# pattern: derive from the worktree folder name
export APP_PORT=<<3000 + N>>
export DATABASE_URL=<<postgres://…/<<db>>_<worktree-name>>>
<<create db command>> && <<migrate>> && <<seed>>
```
Files copied into every new worktree: see `.worktreeinclude` at the repo root.

## 6. Debugging
- Logs: where they are, how to tail them.
- Common failures and fixes (keep this list growing; every "it doesn't start" incident adds a line).

## 7. Environment variables
| Name | Required | Purpose | Where to get it |
|---|---|---|---|
| `<<DATABASE_URL>>` | yes | | local: compose default |

Never commit `.env`. The PreToolUse hook blocks agents from editing it.

## 8. Definition of "the environment works"
All of these pass on a clean checkout: `<<install>>`, `<<migrate>>`, `<<seed>>`, `<<unit>>`, `<<e2e smoke>>`.
