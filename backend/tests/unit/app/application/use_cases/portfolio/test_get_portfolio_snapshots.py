"""Unit tests for GetPortfolioSnapshotsUseCase."""
from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.application.use_cases.portfolio.get_portfolio_snapshots import GetPortfolioSnapshotsUseCase
from app.domain.entities.portfolio import Portfolio
from app.domain.exceptions import PortfolioNotFound


def make_portfolio():
    now = datetime.now(timezone.utc)
    return Portfolio(id=uuid4(), name="P", base_currency="EUR", created_at=now, updated_at=now)


def test_get_snapshots_not_found():
    repo = MagicMock()
    repo.find_with_snapshots.return_value = None
    use_case = GetPortfolioSnapshotsUseCase(repo)
    with pytest.raises(PortfolioNotFound):
        use_case.execute(uuid4())


def test_get_snapshots_success():
    repo = MagicMock()
    portfolio = make_portfolio()
    repo.find_with_snapshots.return_value = portfolio
    use_case = GetPortfolioSnapshotsUseCase(repo)
    result = use_case.execute(portfolio.id)
    assert result is portfolio
    repo.find_with_snapshots.assert_called_once_with(portfolio.id, start_date=None, end_date=None)


def test_get_snapshots_with_dates():
    repo = MagicMock()
    portfolio = make_portfolio()
    repo.find_with_snapshots.return_value = portfolio
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end = datetime(2024, 12, 31, tzinfo=timezone.utc)
    use_case = GetPortfolioSnapshotsUseCase(repo)
    result = use_case.execute(portfolio.id, start_date=start, end_date=end)
    assert result is portfolio
    repo.find_with_snapshots.assert_called_once_with(portfolio.id, start_date=start, end_date=end)
