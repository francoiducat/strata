"""Tests for ApiMapper methods not covered by existing tests."""
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from app.adapters.incoming.api.mappers.api_mapper import ApiMapper
from app.domain.entities.asset import Asset
from app.domain.entities.asset_snapshot import AssetSnapshot
from app.domain.entities.asset_type import AssetType
from app.domain.entities.portfolio import Portfolio
from app.domain.entities.portfolio_snapshot import PortfolioSnapshot


def _now():
    return datetime.now(timezone.utc)


def make_portfolio():
    return Portfolio(
        id=uuid4(), name="P", base_currency="EUR",
        created_at=_now(), updated_at=_now()
    )


def test_to_portfolio_response_list():
    p1, p2 = make_portfolio(), make_portfolio()
    result = ApiMapper.to_portfolio_response_list([p1, p2])
    assert len(result) == 2


def test_to_portfolio_snapshot_response():
    snap = PortfolioSnapshot(
        id=uuid4(), portfolio_id=uuid4(),
        value=Decimal("1000.0"), observed_at=_now()
    )
    result = ApiMapper.to_portfolio_snapshot_response(snap)
    assert str(result.id) == str(snap.id)


def test_to_portfolio_snapshot_response_list():
    snaps = [
        PortfolioSnapshot(id=uuid4(), portfolio_id=uuid4(), value=Decimal("10"), observed_at=_now()),
        PortfolioSnapshot(id=uuid4(), portfolio_id=uuid4(), value=Decimal("20"), observed_at=_now()),
    ]
    result = ApiMapper.to_portfolio_snapshot_response_list(snaps)
    assert len(result) == 2


def test_to_asset_type_response():
    at = AssetType(id=uuid4(), code="CASH", label="Cash")
    result = ApiMapper.to_asset_type_response(at)
    assert result.code == "CASH"


def test_to_asset_snapshot_response_list():
    snaps = [
        AssetSnapshot(id=uuid4(), asset_id=uuid4(), value=Decimal("10"), observed_at=_now()),
        AssetSnapshot(id=uuid4(), asset_id=uuid4(), value=Decimal("20"), observed_at=_now()),
    ]
    result = ApiMapper.to_asset_snapshot_response_list(snaps)
    assert len(result) == 2
