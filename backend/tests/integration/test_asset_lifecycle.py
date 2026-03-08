"""
Integration test: Asset lifecycle journey.
"""


def test_asset_lifecycle(integration_client, seeded_asset_type, seeded_portfolio):
    portfolio_id = seeded_portfolio["id"]
    asset_type_id = str(seeded_asset_type.id)

    # Create asset
    resp = integration_client.post("/api/v1/assets/", json={
        "portfolio_id": portfolio_id,
        "asset_type_id": asset_type_id,
        "name": "My Test Asset",
        "created_by": "test_user"
    })
    assert resp.status_code == 201
    asset_data = resp.json()
    asset_id = asset_data["id"]
    assert asset_data["disposed"] == False

    # Update asset
    resp = integration_client.put(f"/api/v1/assets/{asset_id}", json={
        "name": "Updated Asset",
        "updated_by": "test_user"
    })
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated Asset"

    # Create snapshot
    resp = integration_client.post(f"/api/v1/assets/{asset_id}/snapshots", json={
        "value": "1500.00"
    })
    assert resp.status_code == 201
    assert float(resp.json()["value"]) == 1500.0

    # Dispose asset
    resp = integration_client.put(f"/api/v1/assets/{asset_id}/dispose")
    assert resp.status_code == 200
    assert resp.json()["disposed"] == True

    # Verify disposed via GET
    resp = integration_client.get(f"/api/v1/assets/{asset_id}")
    assert resp.status_code == 200
    assert resp.json()["disposed"] == True
