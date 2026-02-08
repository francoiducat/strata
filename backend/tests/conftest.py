"""Shared pytest fixtures for unit and integration tests."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def dummy_asset_repository(monkeypatch):
    """Provide a simple in-memory fake repository for Asset use-cases.

    This fake implements only the methods used by use-cases in unit tests:
    - find_all
    - find_by_id
    - save
    - delete
    """

    class _FakeAssetRepo:
        def __init__(self):
            self.storage = {}

        def find_all(self):
            return list(self.storage.values())

        def find_by_id(self, id_):
            return self.storage.get(str(id_))

        def save(self, asset):
            self.storage[str(asset.id)] = asset
            return asset

        def delete(self, id_):
            return self.storage.pop(str(id_), None) is not None

    return _FakeAssetRepo()


@pytest.fixture
def dummy_portfolio_repository(monkeypatch):
    class _FakePortfolioRepo:
        def __init__(self):
            self.storage = {}

        def find_all(self):
            return list(self.storage.values())

        def find_by_id(self, id_):
            return self.storage.get(str(id_))

        def save(self, portfolio):
            self.storage[str(portfolio.id)] = portfolio
            return portfolio

        def delete(self, id_):
            return self.storage.pop(str(id_), None) is not None

    return _FakePortfolioRepo()

