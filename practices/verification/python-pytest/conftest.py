"""Shared fixtures for smoke/integration tests.

Pattern: real database in a container (testcontainers) or a dedicated local DB from DATABASE_URL_TEST,
seeded once per session; every test runs in a transaction that is rolled back.
Install: pip install pytest testcontainers[postgres] sqlalchemy
"""
import os
import pytest

@pytest.fixture(scope="session")
def database_url():
    url = os.getenv("DATABASE_URL_TEST")
    if url:
        yield url
        return
    from testcontainers.postgres import PostgresContainer  # optional dependency
    with PostgresContainer("postgres:16") as pg:
        yield pg.get_connection_url()

@pytest.fixture(scope="session")
def seeded_db(database_url):
    # <<run migrations + seed against database_url>>
    # e.g. subprocess.run(["alembic", "upgrade", "head"], env={**os.environ, "DATABASE_URL": database_url}, check=True)
    yield database_url

@pytest.fixture
def dry_run_env(monkeypatch):
    """Pipelines with side effects (email, posts, payments) must honor DRY_RUN=1."""
    monkeypatch.setenv("DRY_RUN", "1")
    yield
