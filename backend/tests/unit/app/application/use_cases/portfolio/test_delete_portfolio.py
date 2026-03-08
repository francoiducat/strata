"""Unit tests for DeletePortfolioUseCase."""
from uuid import uuid4

import pytest

from app.application.use_cases.portfolio.delete_portfolio import DeletePortfolioUseCase
from app.domain.exceptions import PortfolioNotFound


def test_delete_portfolio_success(dummy_portfolio_repository):
    from datetime import datetime, timezone
    from app.domain.entities.portfolio import Portfolio
    now = datetime.now(timezone.utc)
    portfolio = Portfolio(id=uuid4(), name="P", base_currency="EUR", created_at=now, updated_at=now)
    dummy_portfolio_repository.save(portfolio)

    use_case = DeletePortfolioUseCase(dummy_portfolio_repository)
    result = use_case.execute(portfolio.id)
    assert result is None


def test_delete_portfolio_not_found(dummy_portfolio_repository):
    use_case = DeletePortfolioUseCase(dummy_portfolio_repository)
    with pytest.raises(PortfolioNotFound):
        use_case.execute(uuid4())
