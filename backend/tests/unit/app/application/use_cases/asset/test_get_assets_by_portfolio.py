"""Unit tests for GetAssetsByPortfolioUseCase."""
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.application.use_cases.asset.get_assets_by_portfolio import GetAssetsByPortfolioUseCase
from app.domain.entities.portfolio import Portfolio
from app.domain.exceptions import PortfolioNotFound


def make_portfolio():
    now = datetime.now(timezone.utc)
    return Portfolio(id=uuid4(), name="P", base_currency="EUR", created_at=now, updated_at=now)


class FakeAssetRepoWithPortfolio:
    def __init__(self):
        self.storage = {}

    def find_by_id(self, id_):
        return self.storage.get(str(id_))

    def find_by_portfolio(self, portfolio_id):
        return []


def test_get_assets_by_portfolio_not_found(dummy_portfolio_repository):
    asset_repo = FakeAssetRepoWithPortfolio()
    use_case = GetAssetsByPortfolioUseCase(asset_repo, dummy_portfolio_repository)
    with pytest.raises(PortfolioNotFound):
        use_case.execute(uuid4())


def test_get_assets_by_portfolio_success(dummy_portfolio_repository):
    portfolio = make_portfolio()
    dummy_portfolio_repository.save(portfolio)
    asset_repo = FakeAssetRepoWithPortfolio()
    use_case = GetAssetsByPortfolioUseCase(asset_repo, dummy_portfolio_repository)
    result = use_case.execute(portfolio.id)
    assert result == []
