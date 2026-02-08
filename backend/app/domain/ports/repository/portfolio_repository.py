"""
Portfolio Repository Interface (Port)
"""
from abc import abstractmethod
from datetime import datetime
from typing import Optional
from uuid import UUID

from .base_repository import BaseRepository
from app.domain.entities.portfolio import Portfolio


class IPortfolioRepository(BaseRepository[Portfolio]):
    """
    Repository interface for Portfolio aggregate
    """

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Portfolio]:
        """
        Find portfolios by exact name

        Args:
            name: Portfolio name

        Returns:
            Portfolio if found, None otherwise
        """
        pass

    @abstractmethod
    def find_with_assets(self, portfolio_id: UUID) -> Optional[Portfolio]:
        """
        Find portfolios with all its assets eagerly loaded

        Args:
            portfolio_id: UUID of portfolios

        Returns:
            Portfolio with assets loaded, None if not found
        """
        pass

    @abstractmethod
    def find_with_snapshots(
            self,
            portfolio_id: UUID,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> Optional[Portfolio]:
        """
        Find portfolios with snapshots in date range

        Args:
            portfolio_id: UUID of portfolios
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            Portfolio with filtered snapshots, None if not found
        """
        pass

    @abstractmethod
    def count_assets(self, portfolio_id: UUID) -> int:
        """
        Count total assets in portfolios

        Args:
            portfolio_id: UUID of portfolios

        Returns:
            Number of assets (0 if portfolios not found)
        """
        pass