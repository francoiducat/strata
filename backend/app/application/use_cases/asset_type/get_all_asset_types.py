"""
Use Case: Get All Asset Types
"""
from typing import List

from app.domain.entities.asset_type import AssetType
from app.domain.ports.repository import IAssetTypeRepository


class GetAllAssetTypesUseCase:
    """
    Use case for retrieving all asset types.
    """

    def __init__(self, asset_type_repository: IAssetTypeRepository):
        self.asset_type_repository = asset_type_repository

    def execute(self) -> List[AssetType]:
        """
        Fetches all asset types.
        """
        return self.asset_type_repository.find_all()

