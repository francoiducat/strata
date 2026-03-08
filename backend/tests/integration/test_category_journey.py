"""
Integration test: Category hierarchy journey.
"""


def test_category_hierarchy(integration_client):
    """Create root and child categories, verify hierarchy."""
    # Create root category
    resp = integration_client.post("/api/v1/categories/", json={"name": "Finance"})
    assert resp.status_code == 201
    root_id = resp.json()["id"]

    # Create child category
    resp = integration_client.post("/api/v1/categories/", json={
        "name": "Stocks",
        "parent_id": root_id
    })
    assert resp.status_code == 201
    child_id = resp.json()["id"]
    assert resp.json()["parent_id"] == root_id

    # Get children of root
    resp = integration_client.get(f"/api/v1/categories/{root_id}/children")
    assert resp.status_code == 200
    children = resp.json()
    assert len(children) == 1
    assert children[0]["id"] == child_id

    # Try to delete root (has children) — should fail
    resp = integration_client.delete(f"/api/v1/categories/{root_id}")
    assert resp.status_code == 409
    assert resp.json()["code"] == "CATEGORY_HAS_CHILDREN"

    # Delete child first, then root
    resp = integration_client.delete(f"/api/v1/categories/{child_id}")
    assert resp.status_code == 204

    resp = integration_client.delete(f"/api/v1/categories/{root_id}")
    assert resp.status_code == 204


def test_duplicate_category_name(integration_client):
    """Creating a category with a duplicate name returns 409."""
    integration_client.post("/api/v1/categories/", json={"name": "UniqueFinance"})
    resp = integration_client.post("/api/v1/categories/", json={"name": "UniqueFinance"})
    assert resp.status_code == 409
    assert resp.json()["code"] == "DUPLICATE_NAME"
