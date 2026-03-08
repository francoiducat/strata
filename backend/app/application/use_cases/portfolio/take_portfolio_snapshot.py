"""Use Case: Take Portfolio Snapshot"""
from datetime import datetime, timezone
from uuid import UUID, uuid4
from app.domain.entities.portfolio_snapshot import PortfolioSnapshot
from app.domain.exceptions import PortfolioNotFound
from app.domain.ports.repository import IPortfolioRepository


class TakePortfolioSnapshotUseCase:
    """
    Computes the current net worth of a portfolio (sum of latest asset snapshot values)
    and persists it as a PortfolioSnapshot for historical tracking.
    """

    def __init__(self, portfolio_repository: IPortfolioRepository):
        self.portfolio_repository = portfolio_repository

    def execute(self, portfolio_id: UUID) -> PortfolioSnapshot:
        portfolio = self.portfolio_repository.find_with_assets(portfolio_id)
        if portfolio is None:
            raise PortfolioNotFound(f"Portfolio with id {portfolio_id} not found.")

        total_value = portfolio.total_value()

        snapshot = PortfolioSnapshot(
            id=uuid4(),
            portfolio_id=portfolio.id,
            value=total_value,
            observed_at=datetime.now(timezone.utc),
        )
        self.portfolio_repository.save_snapshot(snapshot)
        return snapshot
