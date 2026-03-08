"""
Integration test: Portfolio lifecycle journey.
Tests the full HTTP → use case → repository → in-memory DB round-trip.
"""


def test_create_portfolio_and_get(integration_client):
    """Create a portfolio and verify it can be retrieved."""
    resp = integration_client.post("/api/v1/portfolios/", json={
        "name": "My Test Portfolio",
        "base_currency": "EUR"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "My Test Portfolio"
    assert data["base_currency"] == "EUR"
    assert "id" in data
    portfolio_id = data["id"]

    # Retrieve it
    resp = integration_client.get(f"/api/v1/portfolios/{portfolio_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "My Test Portfolio"


def test_update_portfolio(integration_client):
    """Update a portfolio's name."""
    resp = integration_client.post("/api/v1/portfolios/", json={"name": "Original"})
    assert resp.status_code == 201
    portfolio_id = resp.json()["id"]

    resp = integration_client.put(f"/api/v1/portfolios/{portfolio_id}", json={
        "name": "Updated Name",
        "base_currency": "USD"
    })
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated Name"
    assert resp.json()["base_currency"] == "USD"


def test_portfolio_not_found(integration_client):
    """Non-existent portfolio returns 404 with standard error response."""
    resp = integration_client.get("/api/v1/portfolios/00000000-0000-0000-0000-000000000001")
    assert resp.status_code == 404
    data = resp.json()
    assert data["code"] == "PORTFOLIO_NOT_FOUND"
    assert "status" in data
