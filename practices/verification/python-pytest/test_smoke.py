"""Smoke tests for a Python service or pipeline. Run: pytest -q -x tests/test_smoke.py"""
import subprocess
import sys

def test_imports_and_config_load():
    # The cheapest sensor: the package imports and config parses.
    import <<app>>  # noqa: F401
    from <<app.config>> import settings
    assert settings.<<database_url>>

def test_pipeline_dry_run_processes_a_small_batch(seeded_db, dry_run_env):
    # Pipelines: run the main step on a tiny seeded batch with side effects disabled,
    # then assert on the resulting rows/state rather than on logs.
    from <<app.pipeline>> import run
    result = run(limit=5)
    assert result.processed == 5
    assert result.errors == []
    assert result.sent == 0  # DRY_RUN must not send

def test_cli_entrypoint_help():
    out = subprocess.run([sys.executable, "-m", "<<app>>", "--help"], capture_output=True, text=True)
    assert out.returncode == 0
    assert "usage" in out.stdout.lower()

def test_health_endpoint_if_service(seeded_db):
    try:
        from <<app.main>> import app
    except ImportError:
        return  # not a web service
    from fastapi.testclient import TestClient  # or the framework's client
    client = TestClient(app)
    assert client.get("/<<health>>").status_code == 200
