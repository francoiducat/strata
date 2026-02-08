"""
Transaction Repository Interface (Port)

Repository interface for transaction/ledger style records related to assets.
"""
from abc import abstractmethod
from datetime import datetime
from typing import List
from uuid import UUID

from .base_repository import BaseRepository
from ....domain.entities.transaction import Transaction


class ITransactionRepository(BaseRepository[Transaction]):
    """
    Interface for transactions related to assets (optional feature).
    """

    @abstractmethod
    def find_by_asset(self, asset_id: UUID) -> List[Transaction]:
        """
        Find transactions related to an asset.

        Args:
            asset_id: UUID of asset

        Returns:
            List of transactions (may be empty)
        """
        pass

    @abstractmethod
    def find_between_dates(self, start_date: datetime, end_date: datetime) -> List[Transaction]:
        """
        Find transactions in a date range.

        Returns:
            List of transactions
        """
        pass
