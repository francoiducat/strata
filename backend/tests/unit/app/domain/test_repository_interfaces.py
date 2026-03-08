"""Tests to cover abstract method pass-bodies in repository interfaces."""
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.ports.repository.base_repository import BaseRepository
from app.domain.ports.repository.asset_repository import IAssetRepository
from app.domain.ports.repository.asset_snapshot_repository import IAssetSnapshotRepository
from app.domain.ports.repository.asset_type_repository import IAssetTypeRepository
from app.domain.ports.repository.category_repository import ICategoryRepository
from app.domain.ports.repository.portfolio_repository import IPortfolioRepository
from app.domain.ports.repository.portfolio_snapshot_repository import IPortfolioSnapshotRepository
from app.domain.ports.repository.tag_repository import ITagRepository
from app.domain.ports.repository.transaction_repository import ITransactionRepository


# ---------------------------------------------------------------------------
# Concrete implementations that call super() to cover the abstract pass bodies
# ---------------------------------------------------------------------------

class ConcreteBaseRepo(BaseRepository):
    def save(self, entity): return super().save(entity)
    def find_by_id(self, entity_id): return super().find_by_id(entity_id)
    def find_all(self): return super().find_all()
    def delete(self, entity_id): return super().delete(entity_id)
    def exists(self, entity_id): return super().exists(entity_id)


class ConcreteAssetRepo(IAssetRepository):
    def save(self, entity): return super().save(entity)
    def find_by_id(self, entity_id): return super().find_by_id(entity_id)
    def find_all(self): return super().find_all()
    def delete(self, entity_id): return super().delete(entity_id)
    def exists(self, entity_id): return super().exists(entity_id)
    def find_by_portfolio(self, portfolio_id): return super().find_by_portfolio(portfolio_id)
    def find_by_type(self, asset_type_code): return super().find_by_type(asset_type_code)
    def find_by_category(self, category_id): return super().find_by_category(category_id)
    def find_by_tag(self, tag_id): return super().find_by_tag(tag_id)
    def find_active(self, portfolio_id): return super().find_active(portfolio_id)
    def find_disposed(self, portfolio_id): return super().find_disposed(portfolio_id)
    def find_with_snapshots(self, asset_id, start_date=None, end_date=None): return super().find_with_snapshots(asset_id, start_date, end_date)
    def add_category(self, asset_id, category_id): return super().add_category(asset_id, category_id)
    def remove_category(self, asset_id, category_id): return super().remove_category(asset_id, category_id)
    def add_tag(self, asset_id, tag_id): return super().add_tag(asset_id, tag_id)
    def remove_tag(self, asset_id, tag_id): return super().remove_tag(asset_id, tag_id)


class ConcreteAssetSnapshotRepo(IAssetSnapshotRepository):
    def save(self, entity): return super().save(entity)
    def find_by_id(self, entity_id): return super().find_by_id(entity_id)
    def find_all(self): return super().find_all()
    def delete(self, entity_id): return super().delete(entity_id)
    def exists(self, entity_id): return super().exists(entity_id)
    def get_snapshots(self, asset_id, start_date=None, end_date=None): return super().get_snapshots(asset_id, start_date, end_date)
    def get_latest_snapshot(self, asset_id): return super().get_latest_snapshot(asset_id)


class ConcreteAssetTypeRepo(IAssetTypeRepository):
    def save(self, entity): return super().save(entity)
    def find_by_id(self, entity_id): return super().find_by_id(entity_id)
    def find_all(self): return super().find_all()
    def delete(self, entity_id): return super().delete(entity_id)
    def exists(self, entity_id): return super().exists(entity_id)
    def find_by_code(self, code): return super().find_by_code(code)
    def find_all_codes(self): return super().find_all_codes()


class ConcreteCategoryRepo(ICategoryRepository):
    def save(self, entity): return super().save(entity)
    def find_by_id(self, entity_id): return super().find_by_id(entity_id)
    def find_all(self): return super().find_all()
    def delete(self, entity_id): return super().delete(entity_id)
    def exists(self, entity_id): return super().exists(entity_id)
    def find_by_name(self, name): return super().find_by_name(name)
    def find_root_categories(self): return super().find_root_categories()
    def find_children(self, parent_id): return super().find_children(parent_id)
    def count_assets(self, category_id): return super().count_assets(category_id)


class ConcretePortfolioRepo(IPortfolioRepository):
    def save(self, entity): return super().save(entity)
    def find_by_id(self, entity_id): return super().find_by_id(entity_id)
    def find_all(self): return super().find_all()
    def delete(self, entity_id): return super().delete(entity_id)
    def exists(self, entity_id): return super().exists(entity_id)
    def find_by_name(self, name): return super().find_by_name(name)
    def find_with_assets(self, portfolio_id): return super().find_with_assets(portfolio_id)
    def find_with_snapshots(self, portfolio_id, start_date=None, end_date=None): return super().find_with_snapshots(portfolio_id, start_date, end_date)
    def save_snapshot(self, snapshot): return super().save_snapshot(snapshot)
    def count_assets(self, portfolio_id): return super().count_assets(portfolio_id)


class ConcretePortfolioSnapshotRepo(IPortfolioSnapshotRepository):
    def save(self, entity): return super().save(entity)
    def find_by_id(self, entity_id): return super().find_by_id(entity_id)
    def find_all(self): return super().find_all()
    def delete(self, entity_id): return super().delete(entity_id)
    def exists(self, entity_id): return super().exists(entity_id)
    def get_snapshots(self, portfolio_id, start_date=None, end_date=None): return super().get_snapshots(portfolio_id, start_date, end_date)
    def get_latest_snapshot(self, portfolio_id): return super().get_latest_snapshot(portfolio_id)


class ConcreteTagRepo(ITagRepository):
    def save(self, entity): return super().save(entity)
    def find_by_id(self, entity_id): return super().find_by_id(entity_id)
    def find_all(self): return super().find_all()
    def delete(self, entity_id): return super().delete(entity_id)
    def exists(self, entity_id): return super().exists(entity_id)
    def find_by_name(self, name): return super().find_by_name(name)
    def find_by_asset(self, asset_id): return super().find_by_asset(asset_id)
    def attach_to_asset(self, asset_id, tag_id): return super().attach_to_asset(asset_id, tag_id)
    def detach_from_asset(self, asset_id, tag_id): return super().detach_from_asset(asset_id, tag_id)


class ConcreteTransactionRepo(ITransactionRepository):
    def save(self, entity): return super().save(entity)
    def find_by_id(self, entity_id): return super().find_by_id(entity_id)
    def find_all(self): return super().find_all()
    def delete(self, entity_id): return super().delete(entity_id)
    def exists(self, entity_id): return super().exists(entity_id)
    def find_by_asset(self, asset_id): return super().find_by_asset(asset_id)
    def find_between_dates(self, start_date, end_date): return super().find_between_dates(start_date, end_date)


# ---------------------------------------------------------------------------
# Tests: calling each abstract method via super() covers the pass bodies
# ---------------------------------------------------------------------------

_ID = str(uuid4())
_UUID = uuid4()
_NOW = datetime.now(timezone.utc)


def test_base_repository_abstract_methods():
    repo = ConcreteBaseRepo()
    assert repo.save(None) is None
    assert repo.find_by_id(_ID) is None
    assert repo.find_all() is None
    assert repo.delete(_ID) is None
    assert repo.exists(_ID) is None


def test_asset_repository_abstract_methods():
    repo = ConcreteAssetRepo()
    repo.save(None)
    repo.find_by_id(_ID)
    repo.find_all()
    repo.delete(_ID)
    repo.exists(_ID)
    repo.find_by_portfolio(_UUID)
    repo.find_by_type("EQUITY")
    repo.find_by_category(_UUID)
    repo.find_by_tag(_UUID)
    repo.find_active(_UUID)
    repo.find_disposed(_UUID)
    repo.find_with_snapshots(_UUID)
    repo.add_category(_UUID, _UUID)
    repo.remove_category(_UUID, _UUID)
    repo.add_tag(_UUID, _UUID)
    repo.remove_tag(_UUID, _UUID)


def test_asset_snapshot_repository_abstract_methods():
    repo = ConcreteAssetSnapshotRepo()
    repo.save(None)
    repo.find_by_id(_ID)
    repo.find_all()
    repo.delete(_ID)
    repo.exists(_ID)
    repo.get_snapshots(_UUID)
    repo.get_latest_snapshot(_UUID)


def test_asset_type_repository_abstract_methods():
    repo = ConcreteAssetTypeRepo()
    repo.save(None)
    repo.find_by_id(_ID)
    repo.find_all()
    repo.delete(_ID)
    repo.exists(_ID)
    repo.find_by_code("EQUITY")
    repo.find_all_codes()


def test_category_repository_abstract_methods():
    repo = ConcreteCategoryRepo()
    repo.save(None)
    repo.find_by_id(_ID)
    repo.find_all()
    repo.delete(_ID)
    repo.exists(_ID)
    repo.find_by_name("Stocks")
    repo.find_root_categories()
    repo.find_children(_UUID)
    repo.count_assets(_UUID)


def test_portfolio_repository_abstract_methods():
    repo = ConcretePortfolioRepo()
    repo.save(None)
    repo.find_by_id(_ID)
    repo.find_all()
    repo.delete(_ID)
    repo.exists(_ID)
    repo.find_by_name("My Portfolio")
    repo.find_with_assets(_UUID)
    repo.find_with_snapshots(_UUID)
    repo.save_snapshot(None)
    repo.count_assets(_UUID)


def test_portfolio_snapshot_repository_abstract_methods():
    repo = ConcretePortfolioSnapshotRepo()
    repo.save(None)
    repo.find_by_id(_ID)
    repo.find_all()
    repo.delete(_ID)
    repo.exists(_ID)
    repo.get_snapshots(_UUID)
    repo.get_latest_snapshot(_UUID)


def test_tag_repository_abstract_methods():
    repo = ConcreteTagRepo()
    repo.save(None)
    repo.find_by_id(_ID)
    repo.find_all()
    repo.delete(_ID)
    repo.exists(_ID)
    repo.find_by_name("green")
    repo.find_by_asset(_UUID)
    repo.attach_to_asset(_UUID, _UUID)
    repo.detach_from_asset(_UUID, _UUID)


def test_transaction_repository_abstract_methods():
    repo = ConcreteTransactionRepo()
    repo.save(None)
    repo.find_by_id(_ID)
    repo.find_all()
    repo.delete(_ID)
    repo.exists(_ID)
    repo.find_by_asset(_UUID)
    repo.find_between_dates(_NOW, _NOW)
