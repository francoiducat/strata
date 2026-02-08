from fastapi.testclient import TestClient


def test_get_all_portfolios(client: TestClient):
    resp = client.get('/api/v1/portfolios/')
    assert resp.status_code == 200


def test_create_portfolio_empty_request(client: TestClient):
    resp = client.post('/api/v1/portfolios/', json={})
    assert resp.status_code == 422

