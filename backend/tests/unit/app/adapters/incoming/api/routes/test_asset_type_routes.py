"""Unit tests for asset type routes."""
from unittest.mock import MagicMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.adapters.incoming.api.dependencies.asset_types import get_all_asset_types_use_case, get_asset_type_use_case
from app.domain.exceptions import AssetTypeNotFound


def test_get_all_asset_types():
    mock_use_case = MagicMock()
    mock_use_case.execute.return_value = []
    app.dependency_overrides[get_all_asset_types_use_case] = lambda: mock_use_case
    client = TestClient(app)
    try:
        resp = client.get('/api/v1/asset-types/')
        assert resp.status_code == 200
        assert resp.json() == []
    finally:
        app.dependency_overrides.clear()


def test_get_asset_type_not_found():
    mock_use_case = MagicMock()
    mock_use_case.execute.side_effect = AssetTypeNotFound("Asset type not found")
    app.dependency_overrides[get_asset_type_use_case] = lambda: mock_use_case
    client = TestClient(app)
    try:
        resp = client.get(f'/api/v1/asset-types/{uuid4()}')
        assert resp.status_code == 404
        assert resp.json()['code'] == 'ASSET_TYPE_NOT_FOUND'
    finally:
        app.dependency_overrides.clear()
