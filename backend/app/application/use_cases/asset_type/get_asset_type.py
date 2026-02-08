"""
Use Case: Get Asset Type
"""
from uuid import UUID

from app.domain.entities.asset_type import AssetType
from app.domain.exceptions import AssetTypeNotFound
from app.domain.ports.repository import IAssetTypeRepository


class GetAssetTypeUseCase:
    """
    Use case for retrieving a single asset type.
    """

    def __init__(self, asset_type_repository: IAssetTypeRepository):
        self.asset_type_repository = asset_type_repository

    def execute(self, asset_type_id: UUID) -> AssetType:
        """
        Fetches an asset type by its ID.

        Raises:
            AssetTypeNotFound: If no asset type with the given ID is found.
        """
        asset_type = self.asset_type_repository.find_by_id(asset_type_id)
        if asset_type is None:
            raise AssetTypeNotFound(f"AssetType with id {asset_type_id} not found.")
        return asset_type

