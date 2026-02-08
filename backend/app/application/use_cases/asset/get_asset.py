"""
Use Case: Get Asset
"""
from uuid import UUID

from app.domain.entities.asset import Asset
from app.domain.exceptions import AssetNotFound
from app.domain.ports.repository import IAssetRepository


class GetAssetUseCase:
    """
    Use case for retrieving a single asset.
    """

    def __init__(self, asset_repository: IAssetRepository):
        self.asset_repository = asset_repository

    def execute(self, asset_id: UUID) -> Asset:
        """
        Fetches an asset by its ID.

        Raises:
            AssetNotFound: If no asset with the given ID is found.
        """
        asset = self.asset_repository.find_by_id(asset_id)
        if asset is None:
            raise AssetNotFound(f"Asset with id {asset_id} not found.")
        return asset
