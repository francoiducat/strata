"""Unit tests for app/main.py uncovered lines."""
import asyncio
from unittest.mock import MagicMock

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from app.main import app, log_exceptions


def test_root_endpoint(app_client):
    resp = app_client.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()


def test_lifespan_startup_shutdown(capsys):
    with TestClient(app) as client:
        resp = client.get("/")
        assert resp.status_code == 200
    captured = capsys.readouterr()
    assert "starting" in captured.out.lower()
    assert "shutting down" in captured.out.lower()


def test_middleware_unhandled_exception():
    @app.get("/test-internal-error-route")
    def _error_route():
        raise RuntimeError("boom")

    client = TestClient(app, raise_server_exceptions=False)
    resp = client.get("/test-internal-error-route")
    assert resp.status_code == 500
    data = resp.json()
    assert data["code"] == "INTERNAL_ERROR"


def test_middleware_domain_exception_reraised():
    """Cover line 56: the `raise` for domain exceptions caught by the middleware."""
    from app.domain.exceptions import AssetNotFound

    async def run():
        request = MagicMock(spec=Request)

        async def call_next_raises(req):
            raise AssetNotFound("test asset not found")

        with pytest.raises(AssetNotFound):
            await log_exceptions(request, call_next_raises)

    asyncio.run(run())
