"""
Portfolio Snapshot Repository Interface (Port)

Defines operations to retrieve historical snapshots of Portfolios.
"""
from abc import abstractmethod
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from .base_repository import BaseRepository
from ....domain.entities.portfolio_snapshot import PortfolioSnapshot


class IPortfolioSnapshotRepository(BaseRepository[PortfolioSnapshot]):
    """
    Repository interface for Portfolio snapshots (time-series data).
    """

    @abstractmethod
    def get_snapshots(
            self,
            portfolio_id: UUID,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> List[PortfolioSnapshot]:
        """
        Retrieve snapshots for a portfolios in a date range.

        Args:
            portfolio_id: UUID of portfolios
            start_date: Inclusive start date
            end_date: Inclusive end date

        Returns:
            List of PortfolioSnapshot objects (may be empty)
        """
        pass

    @abstractmethod
    def get_latest_snapshot(self, portfolio_id: UUID) -> Optional[PortfolioSnapshot]:
        """
        Retrieve the most recent snapshot for a portfolios.

        Args:
            portfolio_id: UUID of portfolios

        Returns:
            PortfolioSnapshot or None if no snapshots exist
        """
        pass
