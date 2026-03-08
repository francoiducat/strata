"""Tests for persistence_mapper with load_snapshots and load_assets branches."""
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

from app.adapters.outgoing.persistence.mappers.persistence_mapper import PersistenceMapper


def _now():
    return datetime.now(timezone.utc)


def make_portfolio_orm():
    m = MagicMock()
    m.id = str(uuid4())
    m.name = "Portfolio"
    m.base_currency = "EUR"
    m.created_at = _now()
    m.updated_at = _now()
    m.assets = []
    return m


def make_asset_type_orm():
    m = MagicMock()
    m.id = str(uuid4())
    m.code = "EQUITY"
    m.label = "Equity"
    return m


def make_asset_snapshot_orm():
    m = MagicMock()
    m.id = str(uuid4())
    m.asset_id = str(uuid4())
    m.value = Decimal("100.0")
    m.observed_at = _now()
    return m


def make_asset_orm(portfolio_orm=None, with_snapshots=False):
    m = MagicMock()
    m.id = str(uuid4())
    m.name = "Asset"
    m.portfolio = portfolio_orm or make_portfolio_orm()
    m.asset_type = make_asset_type_orm()
    m.quantity = None
    m.disposed = False
    m.tags = []
    m.categories = []
    m.created_at = _now()
    m.updated_at = _now()
    m.created_by = "user"
    m.updated_by = "user"
    m.snapshots = [make_asset_snapshot_orm()] if with_snapshots else []
    return m


def test_asset_with_portfolio_load_snapshots_true():
    """Covers the load_snapshots=True branch in _asset_with_portfolio."""
    portfolio_orm = make_portfolio_orm()
    from app.domain.entities.portfolio import Portfolio
    portfolio = Portfolio(
        id=uuid4(), name="P", base_currency="EUR",
        created_at=_now(), updated_at=_now()
    )
    asset_orm = make_asset_orm(with_snapshots=True)

    asset = PersistenceMapper._asset_with_portfolio(asset_orm, portfolio, load_snapshots=True)
    assert len(asset.snapshots) == 1


def test_asset_with_portfolio_load_snapshots_false():
    """No snapshots loaded when load_snapshots=False."""
    from app.domain.entities.portfolio import Portfolio
    portfolio = Portfolio(
        id=uuid4(), name="P", base_currency="EUR",
        created_at=_now(), updated_at=_now()
    )
    asset_orm = make_asset_orm(with_snapshots=True)
    asset = PersistenceMapper._asset_with_portfolio(asset_orm, portfolio, load_snapshots=False)
    assert len(asset.snapshots) == 0


def test_portfolio_to_domain_load_assets_true():
    """Covers the load_assets=True branch in portfolio_to_domain."""
    portfolio_orm = make_portfolio_orm()
    asset_orm = make_asset_orm(portfolio_orm=portfolio_orm, with_snapshots=True)
    portfolio_orm.assets = [asset_orm]

    portfolio = PersistenceMapper.portfolio_to_domain(portfolio_orm, load_assets=True)
    assert len(portfolio.assets) == 1
    assert len(portfolio.assets[0].snapshots) == 1


def test_portfolio_to_domain_load_assets_false():
    """No assets when load_assets=False."""
    portfolio_orm = make_portfolio_orm()
    asset_orm = make_asset_orm()
    portfolio_orm.assets = [asset_orm]

    portfolio = PersistenceMapper.portfolio_to_domain(portfolio_orm, load_assets=False)
    assert len(portfolio.assets) == 0
