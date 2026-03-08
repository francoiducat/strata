"""Unit tests for GetAllPortfoliosUseCase."""
from datetime import datetime, timezone
from uuid import uuid4

from app.application.use_cases.portfolio.get_all_portfolios import GetAllPortfoliosUseCase
from app.domain.entities.portfolio import Portfolio


def make_portfolio():
    now = datetime.now(timezone.utc)
    return Portfolio(id=uuid4(), name="P", base_currency="EUR", created_at=now, updated_at=now)


def test_get_all_portfolios_empty(dummy_portfolio_repository):
    use_case = GetAllPortfoliosUseCase(dummy_portfolio_repository)
    result = use_case.execute()
    assert result == []


def test_get_all_portfolios_with_items(dummy_portfolio_repository):
    p1 = make_portfolio()
    p2 = make_portfolio()
    dummy_portfolio_repository.save(p1)
    dummy_portfolio_repository.save(p2)
    use_case = GetAllPortfoliosUseCase(dummy_portfolio_repository)
    result = use_case.execute()
    assert len(result) == 2
