"""
Asset Repository Interface
"""
from abc import abstractmethod
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from app.domain.entities.asset import Asset
from .base_repository import BaseRepository


class IAssetRepository(BaseRepository[Asset]):
    """
    Interface for the Asset repository, extending the base repository
    with any asset-specific persistence methods.
    """

    @abstractmethod
    def find_by_portfolio(self, portfolio_id: UUID) -> List[Asset]:
        """
        Find all assets in a portfolios

        Args:
            portfolio_id: UUID of portfolios

        Returns:
            List of assets (can be empty)
        """
        pass

    @abstractmethod
    def find_by_type(self, asset_type_code: str) -> List[Asset]:
        """
        Find all assets of a specific type

        Args:
            asset_type_code: Asset type code (e.g., "CASH", "REAL_ESTATE")

        Returns:
            List of assets (can be empty)
        """
        pass

    @abstractmethod
    def find_by_category(self, category_id: UUID) -> List[Asset]:
        """
        Find all assets in a category

        Args:
            category_id: UUID of category

        Returns:
            List of assets (can be empty)
        """
        pass

    @abstractmethod
    def find_by_tag(self, tag_id: UUID) -> List[Asset]:
        """
        Find all assets with a specific tag

        Args:
            tag_id: UUID of tag

        Returns:
            List of assets (can be empty)
        """
        pass

    @abstractmethod
    def find_active(self, portfolio_id: UUID) -> List[Asset]:
        """
        Find all non-disposed assets in a portfolios

        Args:
            portfolio_id: UUID of portfolios

        Returns:
            List of active assets (disposed=False)
        """
        pass

    @abstractmethod
    def find_disposed(self, portfolio_id: UUID) -> List[Asset]:
        """
        Find all disposed assets in a portfolios

        Args:
            portfolio_id: UUID of portfolios

        Returns:
            List of disposed assets (disposed=True)
        """
        pass

    @abstractmethod
    def find_with_snapshots(
            self,
            asset_id: UUID,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> Optional[Asset]:
        """
        Find asset with snapshots in date range

        Args:
            asset_id: UUID of asset
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            Asset with filtered snapshots, None if not found
        """
        pass

    @abstractmethod
    def add_category(self, asset_id: UUID, category_id: UUID) -> bool:
        """
        Add category to asset

        Args:
            asset_id: UUID of asset
            category_id: UUID of category

        Returns:
            True if added, False if asset/category not found
        """
        pass

    @abstractmethod
    def remove_category(self, asset_id: UUID, category_id: UUID) -> bool:
        """
        Remove category from asset

        Args:
            asset_id: UUID of asset
            category_id: UUID of category

        Returns:
            True if removed, False if not found
        """
        pass

    @abstractmethod
    def add_tag(self, asset_id: UUID, tag_id: UUID) -> bool:
        """
        Add tag to asset

        Args:
            asset_id: UUID of asset
            tag_id: UUID of tag

        Returns:
            True if added, False if asset/tag not found
        """
        pass

    @abstractmethod
    def remove_tag(self, asset_id: UUID, tag_id: UUID) -> bool:
        """
        Remove tag from asset

        Args:
            asset_id: UUID of asset
            tag_id: UUID of tag

        Returns:
            True if removed, False if not found
        """
        pass