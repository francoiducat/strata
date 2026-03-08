from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.main import app
from app.adapters.incoming.api.dependencies.assets import get_all_assets_use_case, get_asset_use_case
from app.domain.exceptions import AssetNotFound


def test_get_all_assets():
    mock_use_case = MagicMock()
    mock_use_case.execute.return_value = []
    app.dependency_overrides[get_all_assets_use_case] = lambda: mock_use_case
    client = TestClient(app)
    try:
        resp = client.get('/api/v1/assets/')
        assert resp.status_code == 200
        assert resp.json() == []
    finally:
        app.dependency_overrides.clear()


def test_get_asset_by_id_not_found():
    mock_use_case = MagicMock()
    mock_use_case.execute.side_effect = AssetNotFound("Asset not found")
    app.dependency_overrides[get_asset_use_case] = lambda: mock_use_case
    client = TestClient(app)
    try:
        resp = client.get('/api/v1/assets/741a4337-9a39-4e9e-be7b-4ce9e5e14c7c')
        assert resp.status_code == 404
    finally:
        app.dependency_overrides.clear()

