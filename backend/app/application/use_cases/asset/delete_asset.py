"""
Use Case: Delete Asset
"""
from uuid import UUID

from app.domain.exceptions import AssetNotFound
from app.domain.ports.repository import IAssetRepository


class DeleteAssetUseCase:
    """Use case for deleting an asset by id."""

    def __init__(self, asset_repository: IAssetRepository):
        self.asset_repository = asset_repository

    def execute(self, asset_id: UUID) -> None:
        """Delete the asset; raise AssetNotFound if asset does not exist."""
        deleted = self.asset_repository.delete(str(asset_id))
        if not deleted:
            raise AssetNotFound(f"Asset with id {asset_id} not found.")
        return None
