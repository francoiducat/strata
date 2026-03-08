"""Unit tests for TakePortfolioSnapshotUseCase."""
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.application.use_cases.portfolio.take_portfolio_snapshot import TakePortfolioSnapshotUseCase
from app.domain.entities.portfolio import Portfolio
from app.domain.exceptions import PortfolioNotFound


def make_portfolio(with_assets=False):
    now = datetime.now(timezone.utc)
    p = Portfolio(id=uuid4(), name="My Portfolio", base_currency="EUR", created_at=now, updated_at=now)
    return p


def test_take_snapshot_portfolio_not_found():
    repo = MagicMock()
    repo.find_with_assets.return_value = None
    use_case = TakePortfolioSnapshotUseCase(repo)
    with pytest.raises(PortfolioNotFound):
        use_case.execute(uuid4())


def test_take_snapshot_success():
    repo = MagicMock()
    portfolio = make_portfolio()
    repo.find_with_assets.return_value = portfolio
    repo.save_snapshot.return_value = None

    use_case = TakePortfolioSnapshotUseCase(repo)
    snapshot = use_case.execute(portfolio.id)

    assert snapshot.portfolio_id == portfolio.id
    assert snapshot.value == Decimal("0")
    repo.save_snapshot.assert_called_once_with(snapshot)
