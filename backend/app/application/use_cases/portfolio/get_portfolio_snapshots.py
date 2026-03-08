"""Use Case: Get Portfolio Snapshots"""
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.domain.entities.portfolio import Portfolio
from app.domain.exceptions import PortfolioNotFound
from app.domain.ports.repository import IPortfolioRepository


class GetPortfolioSnapshotsUseCase:
    """Retrieves historical portfolio snapshots for charting net worth over time."""

    def __init__(self, portfolio_repository: IPortfolioRepository):
        self.portfolio_repository = portfolio_repository

    def execute(
        self,
        portfolio_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Portfolio:
        portfolio = self.portfolio_repository.find_with_snapshots(
            portfolio_id, start_date=start_date, end_date=end_date
        )
        if portfolio is None:
            raise PortfolioNotFound(f"Portfolio with id {portfolio_id} not found.")
        return portfolio
