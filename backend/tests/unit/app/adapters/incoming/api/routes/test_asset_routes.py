# Mirrored test location for asset routes (copy)
from fastapi.testclient import TestClient


def test_get_all_assets(client: TestClient):
    resp = client.get('/api/v1/assets/')
    assert resp.status_code == 200


def test_get_asset_by_id_not_found(client: TestClient):
    resp = client.get('/api/v1/assets/741a4337-9a39-4e9e-be7b-4ce9e5e14c7c')
    assert resp.status_code == 404

