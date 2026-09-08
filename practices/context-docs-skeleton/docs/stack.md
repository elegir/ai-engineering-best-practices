# Stack

<!-- Fill every row. "What it is for" must be one plain sentence a new teammate understands. Pin versions; the agent must not guess. -->

## Runtime and language

| Component | Version | What it is for | Notes / gotchas |
|---|---|---|---|
| <<Language, e.g. Node.js>> | <<20.x>> | <<runtime for the API>> | <<use nvm; .nvmrc present>> |

## Frameworks and core libraries

| Library | Version | What it is for | Where it is used |
|---|---|---|---|
| <<Express / FastAPI / WordPress>> | | | |
| <<ORM, e.g. Prisma / SQLAlchemy>> | | | |
| <<Validation, e.g. zod / pydantic>> | | | |

## Data stores and infrastructure

| Service | Version | Purpose | Local | Production |
|---|---|---|---|---|
| <<PostgreSQL>> | <<16>> | <<primary DB>> | <<docker compose service `db`>> | <<managed instance>> |
| <<Redis / queue>> | | | | |

## Tooling

| Tool | Purpose | Command |
|---|---|---|
| Package manager | | `<<npm ci / pip install -r requirements.txt / composer install>>` |
| Formatter | | `<<biome format . / ruff format .>>` |
| Linter | | `<<biome lint . / ruff check .>>` |
| Type checker | | `<<tsc --noEmit / mypy .>>` |
| Unit tests | | `<<npm test / pytest>>` |
| E2E tests | | `<<npx playwright test / hurl --test tests/api>>` |
| CI | | <<GitHub Actions workflow file>> |

## External services and APIs

| Service | Used for | Auth | Sandbox available? |
|---|---|---|---|
| <<Stripe / SendGrid / OpenAI>> | | <<env var name, never the value>> | |

## Do not use

<!-- Libraries or patterns deliberately avoided, with the reason (link an ADR if one exists). Agents will otherwise reintroduce them. -->
- <<`moment` — use `date-fns`; see decisions/0003.>>
