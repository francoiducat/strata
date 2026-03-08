"""
Use Case: Take Portfolio Snapshot
"""
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

from app.domain.exceptions import PortfolioNotFound
from app.domain.ports.repository import IPortfolioRepository
from app.adapters.outgoing.persistence.models.portfolio_snapshot import PortfolioSnapshotModel


class TakePortfolioSnapshotUseCase:
    """
    Computes the current net worth of a portfolio (sum of latest asset snapshot values)
    and persists it as a PortfolioSnapshotModel for historical tracking.
    """

    def __init__(self, portfolio_repository: IPortfolioRepository):
        self.portfolio_repository = portfolio_repository

    def execute(self, portfolio_id: UUID) -> PortfolioSnapshotModel:
        """
        Load portfolio with assets + snapshots, compute total value, and save a snapshot.

        Raises:
            PortfolioNotFound: If no portfolio with the given ID exists.
        """
        portfolio = self.portfolio_repository.find_with_assets(portfolio_id)
        if portfolio is None:
            raise PortfolioNotFound(f"Portfolio with id {portfolio_id} not found.")

        loaded_assets = getattr(portfolio, "assets", None) or []
        total_value = sum(
            (
                Decimal(str(asset.snapshots[0].value))
                for asset in loaded_assets
                if not asset.disposed and asset.snapshots
            ),
            Decimal("0"),
        )

        snapshot = PortfolioSnapshotModel(
            id=str(uuid4()),
            portfolio_id=str(portfolio_id),
            value=total_value,
            observed_at=datetime.now(timezone.utc),
        )
        self.portfolio_repository.save_snapshot(snapshot)
        return snapshot
