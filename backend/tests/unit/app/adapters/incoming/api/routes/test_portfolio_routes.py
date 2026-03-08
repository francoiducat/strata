from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.main import app
from app.adapters.incoming.api.dependencies.portfolios import get_all_portfolios_use_case, create_portfolio_use_case


def test_get_all_portfolios():
    mock_use_case = MagicMock()
    mock_use_case.execute.return_value = []
    app.dependency_overrides[get_all_portfolios_use_case] = lambda: mock_use_case
    client = TestClient(app)
    try:
        resp = client.get('/api/v1/portfolios/')
        assert resp.status_code == 200
        assert resp.json() == []
    finally:
        app.dependency_overrides.clear()


def test_create_portfolio_empty_request():
    client = TestClient(app)
    try:
        resp = client.post('/api/v1/portfolios/', json={})
        assert resp.status_code == 422
    finally:
        app.dependency_overrides.clear()

