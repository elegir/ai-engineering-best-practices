# Infrastructure isolation per worktree

Worktrees isolate **files**, not infrastructure. Two worktrees sharing one database or one port still collide. Pick the pattern for the repo's engine and paste the result into `docs/development-guide.md` §5.

## Ports
Derive from the slug (the scripts do this): `APP_PORT = BASE + hash(slug) % 900`. Read `APP_PORT` in the app config; never hard-code 3000. For Docker Compose, use `${APP_PORT}:3000` in `ports:` and pass `-p <project-name>` (`COMPOSE_PROJECT_NAME=<repo>-<slug>`) so container names don't clash.

## PostgreSQL (one server, one DB per worktree)
```bash
createdb "${DB_NAME}"                      # or: psql -c "CREATE DATABASE ${DB_NAME}"
DATABASE_URL=postgres://user:pass@localhost:5432/${DB_NAME}
dropdb "${DB_NAME}"                        # on removal
```
Alternative: one DB, one **schema** per worktree (`?options=-csearch_path%3D${SAFE}`) when creating databases is restricted.

## MySQL / MariaDB
```bash
mysql -e "CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\`"
DATABASE_URL=mysql://user:pass@localhost:3306/${DB_NAME}
```

## SQLite
`DATABASE_PATH=./data/${SAFE}.sqlite` — file per worktree, nothing else to do.

## WordPress (local)
Fastest: **wp-env** or Docker with `COMPOSE_PROJECT_NAME=<repo>-<slug>` and a distinct `WORDPRESS_DB_NAME`; import the same seed dump into each. Or `wp db export`/`import` into `${DB_NAME}` and set `DB_NAME` in `wp-config.php` from an env var.

## Queues / caches
Redis: use a distinct DB index (`redis://localhost:6379/${hash % 15}`) or key prefix `${SAFE}:`. Local queues (BullMQ, Celery): prefix queue names with the slug.

## Rule of thumb
If it holds state or listens on a port, it needs a per-worktree name. Everything else can be shared.
