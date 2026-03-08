"""Shared pytest fixtures for unit and integration tests."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def app_client() -> TestClient:
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

        def add_tag(self, asset_id, tag_id):
            asset = self.find_by_id(asset_id)
            if not asset:
                return False
            if not hasattr(asset, '_tags'):
                asset._tags = set()
            asset._tags.add(str(tag_id))
            return True

        def remove_tag(self, asset_id, tag_id):
            asset = self.find_by_id(asset_id)
            if not asset or not hasattr(asset, '_tags'):
                return False
            asset._tags.discard(str(tag_id))
            return True

        def add_category(self, asset_id, category_id):
            return self.find_by_id(asset_id) is not None

        def remove_category(self, asset_id, category_id):
            return self.find_by_id(asset_id) is not None

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



@pytest.fixture
def dummy_category_repository():
    class _FakeCategoryRepo:
        def __init__(self):
            self.storage = {}

        def find_all(self):
            return list(self.storage.values())

        def find_by_id(self, id_):
            return self.storage.get(str(id_))

        def find_by_name(self, name):
            return next((v for v in self.storage.values() if v.name == name), None)

        def find_children(self, parent_id):
            return [v for v in self.storage.values() if getattr(v, 'parent_id', None) == str(parent_id)]

        def save(self, entity):
            self.storage[str(entity.id)] = entity
            return entity

        def delete(self, id_):
            return self.storage.pop(str(id_), None) is not None

    return _FakeCategoryRepo()


@pytest.fixture
def dummy_tag_repository():
    class _FakeTagRepo:
        def __init__(self):
            self.storage = {}

        def find_all(self):
            return list(self.storage.values())

        def find_by_id(self, id_):
            return self.storage.get(str(id_))

        def find_by_name(self, name):
            return next((v for v in self.storage.values() if v.name == name), None)

        def save(self, entity):
            self.storage[str(entity.id)] = entity
            return entity

        def delete(self, id_):
            return self.storage.pop(str(id_), None) is not None

    return _FakeTagRepo()


@pytest.fixture
def dummy_asset_snapshot_repository():
    class _FakeSnapshotRepo:
        def __init__(self):
            self.storage = {}

        def find_all(self):
            return list(self.storage.values())

        def find_by_id(self, id_):
            return self.storage.get(str(id_))

        def save(self, entity):
            self.storage[str(entity.id)] = entity
            return entity

        def delete(self, id_):
            return self.storage.pop(str(id_), None) is not None

        def get_snapshots(self, asset_id, start_date=None, end_date=None):
            return [v for v in self.storage.values() if v.asset_id == str(asset_id)]

        def get_latest_snapshot(self, asset_id):
            snapshots = self.get_snapshots(asset_id)
            return max(snapshots, key=lambda s: s.observed_at) if snapshots else None

    return _FakeSnapshotRepo()
