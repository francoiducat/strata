"""Unit tests for UpdatePortfolioUseCase."""
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.application.use_cases.portfolio.update_portfolio import UpdatePortfolioUseCase, UpdatePortfolioCommand
from app.domain.entities.portfolio import Portfolio
from app.domain.exceptions import PortfolioNotFound


def make_portfolio():
    now = datetime.now(timezone.utc)
    return Portfolio(id=uuid4(), name="Old Name", base_currency="EUR", created_at=now, updated_at=now)


def test_update_portfolio_not_found(dummy_portfolio_repository):
    use_case = UpdatePortfolioUseCase(dummy_portfolio_repository)
    cmd = UpdatePortfolioCommand(portfolio_id=uuid4(), name="New", base_currency="USD")
    with pytest.raises(PortfolioNotFound):
        use_case.execute(cmd)


def test_update_portfolio_success(dummy_portfolio_repository):
    portfolio = make_portfolio()
    dummy_portfolio_repository.save(portfolio)
    use_case = UpdatePortfolioUseCase(dummy_portfolio_repository)
    cmd = UpdatePortfolioCommand(portfolio_id=portfolio.id, name="New Name", base_currency="USD")
    result = use_case.execute(cmd)
    assert result.name == "New Name"
    assert result.base_currency == "USD"
