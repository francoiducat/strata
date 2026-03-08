"""Unit tests for CreateAssetUseCase."""
import pytest
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.use_cases.asset.create_asset import CreateAssetUseCase, CreateAssetRequest
from app.domain.entities.asset_type import AssetType
from app.domain.entities.portfolio import Portfolio
from app.domain.exceptions import PortfolioNotFound, AssetTypeNotFound


def make_fake_portfolio(id_=None):
    pid = id_ or uuid4()
    now = datetime.now(timezone.utc)
    return Portfolio(id=pid, name="Test Portfolio", base_currency="EUR", created_at=now, updated_at=now)


def make_fake_asset_type(id_=None):
    return AssetType(id=id_ or uuid4(), code="EQUITY", label="Equity")


def test_create_asset_success(dummy_asset_repository, dummy_portfolio_repository):
    asset_type_repo = MagicMock()

    portfolio_id = uuid4()
    asset_type_id = uuid4()

    portfolio = make_fake_portfolio(portfolio_id)
    dummy_portfolio_repository.save(portfolio)

    asset_type = make_fake_asset_type(asset_type_id)
    asset_type_repo.find_by_id.return_value = asset_type

    use_case = CreateAssetUseCase(dummy_asset_repository, dummy_portfolio_repository, asset_type_repo)
    command = CreateAssetRequest(
        portfolio_id=portfolio_id,
        asset_type_id=asset_type_id,
        name="Test Asset",
        quantity=Decimal("10.0"),
        created_by="test-user",
    )
    result = use_case.execute(command)

    assert result.id is not None
    assert result.name == "Test Asset"
    assert result.portfolio.id == portfolio_id
    assert result.asset_type.id == asset_type_id


def test_create_asset_portfolio_not_found(dummy_asset_repository, dummy_portfolio_repository):
    asset_type_repo = MagicMock()
    use_case = CreateAssetUseCase(dummy_asset_repository, dummy_portfolio_repository, asset_type_repo)
    command = CreateAssetRequest(
        portfolio_id=uuid4(),
        asset_type_id=uuid4(),
        name="Test Asset",
        created_by="test-user",
    )
    with pytest.raises(PortfolioNotFound):
        use_case.execute(command)


def test_create_asset_asset_type_not_found(dummy_asset_repository, dummy_portfolio_repository):
    asset_type_repo = MagicMock()
    asset_type_repo.find_by_id.return_value = None

    portfolio_id = uuid4()
    portfolio = make_fake_portfolio(portfolio_id)
    dummy_portfolio_repository.save(portfolio)

    use_case = CreateAssetUseCase(dummy_asset_repository, dummy_portfolio_repository, asset_type_repo)
    command = CreateAssetRequest(
        portfolio_id=portfolio_id,
        asset_type_id=uuid4(),
        name="Test Asset",
        created_by="test-user",
    )
    with pytest.raises(AssetTypeNotFound):
        use_case.execute(command)
