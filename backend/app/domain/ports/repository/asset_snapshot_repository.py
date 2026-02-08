"""
Asset Snapshot Repository Interface (Port)

Defines operations to retrieve and persist historical snapshots for Assets.
"""
from abc import abstractmethod
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from .base_repository import BaseRepository
from ....domain.entities.asset_snapshot import AssetSnapshot


class IAssetSnapshotRepository(BaseRepository[AssetSnapshot]):
    """
    Repository interface for Asset snapshots (time-series data).
    """

    @abstractmethod
    def get_snapshots(
            self,
            asset_id: UUID,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> List[AssetSnapshot]:
        """
        Retrieve snapshots for an asset in a date range.

        Args:
            asset_id: UUID of asset
            start_date: Inclusive start date
            end_date: Inclusive end date

        Returns:
            List of AssetSnapshot objects (may be empty)
        """
        pass

    @abstractmethod
    def get_latest_snapshot(self, asset_id: UUID) -> Optional[AssetSnapshot]:
        """
        Retrieve the most recent snapshot for an asset.

        Args:
            asset_id: UUID of asset

        Returns:
            AssetSnapshot or None if no snapshots exist
        """
        pass
