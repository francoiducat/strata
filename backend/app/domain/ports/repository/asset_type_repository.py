"""
AssetType Repository Interface
"""
from abc import abstractmethod
from typing import Optional, List

from ....domain.entities.asset_type import AssetType
from .base_repository import BaseRepository


class IAssetTypeRepository(BaseRepository[AssetType]):
    """
    Interface for the AssetType repository.
    """

    @abstractmethod
    def find_by_code(self, code: str) -> Optional[AssetType]:
        """
        Find asset type by code

        Args:
            code: Asset type code (e.g., "CASH", "REAL_ESTATE")

        Returns:
            AssetType if found, None otherwise
        """
        pass

    @abstractmethod
    def find_all_codes(self) -> List[str]:
        """
        Get all asset type codes

        Returns:
            List of all asset type codes
        """
        pass