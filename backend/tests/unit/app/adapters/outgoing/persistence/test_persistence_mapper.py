"""Tests for the PersistenceMapper domain→ORM methods."""
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from app.adapters.outgoing.persistence.mappers.persistence_mapper import PersistenceMapper
from app.domain.entities.asset import Asset
from app.domain.entities.asset_snapshot import AssetSnapshot
from app.domain.entities.asset_type import AssetType
from app.domain.entities.category import Category
from app.domain.entities.portfolio import Portfolio
from app.domain.entities.portfolio_snapshot import PortfolioSnapshot
from app.domain.entities.tag import Tag


def _now():
    return datetime.now(timezone.utc)


def make_portfolio():
    return Portfolio(
        id=uuid4(), name="Portfolio", base_currency="EUR",
        created_at=_now(), updated_at=_now()
    )


def make_asset_type():
    return AssetType(id=uuid4(), code="EQUITY", label="Equity")


def make_asset():
    return Asset(
        id=uuid4(), name="Asset1",
        asset_type=make_asset_type(),
        portfolio=make_portfolio(),
        created_at=_now(), updated_at=_now(),
        created_by="user", updated_by="user",
    )


def test_tag_to_orm():
    tag = Tag(id=uuid4(), name="crypto")
    model = PersistenceMapper.tag_to_orm(tag)
    assert model.id == str(tag.id)
    assert model.name == "crypto"


def test_category_to_orm_without_parent():
    cat = Category(id=uuid4(), name="Stocks")
    model = PersistenceMapper.category_to_orm(cat)
    assert model.id == str(cat.id)
    assert model.name == "Stocks"
    assert model.parent_id is None


def test_category_to_orm_with_parent():
    parent = Category(id=uuid4(), name="Root")
    child = Category(id=uuid4(), name="Child", parent=parent)
    model = PersistenceMapper.category_to_orm(child)
    assert model.parent_id == str(parent.id)


def test_portfolio_to_orm():
    portfolio = make_portfolio()
    model = PersistenceMapper.portfolio_to_orm(portfolio)
    assert model.id == str(portfolio.id)
    assert model.name == portfolio.name
    assert model.base_currency == "EUR"
    assert model.created_at == portfolio.created_at
    assert model.updated_at == portfolio.updated_at


def test_asset_to_orm():
    asset = make_asset()
    model = PersistenceMapper.asset_to_orm(asset)
    assert model.id == str(asset.id)
    assert model.portfolio_id == str(asset.portfolio.id)
    assert model.asset_type_id == str(asset.asset_type.id)
    assert model.name == asset.name
    assert model.disposed == asset.disposed


def test_asset_snapshot_to_orm():
    snap = AssetSnapshot(
        id=uuid4(), asset_id=uuid4(),
        value=Decimal("123.45"), observed_at=_now()
    )
    model = PersistenceMapper.asset_snapshot_to_orm(snap)
    assert model.id == str(snap.id)
    assert model.asset_id == str(snap.asset_id)
    assert model.value == snap.value
    assert model.observed_at == snap.observed_at


def test_portfolio_snapshot_to_orm():
    snap = PortfolioSnapshot(
        id=uuid4(), portfolio_id=uuid4(),
        value=Decimal("999.99"), observed_at=_now()
    )
    model = PersistenceMapper.portfolio_snapshot_to_orm(snap)
    assert model.id == str(snap.id)
    assert model.portfolio_id == str(snap.portfolio_id)
    assert model.value == snap.value
    assert model.observed_at == snap.observed_at
