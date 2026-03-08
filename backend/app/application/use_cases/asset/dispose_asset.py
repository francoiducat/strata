"""Use Case: Dispose Asset"""
from datetime import datetime, timezone
from uuid import UUID
from app.domain.exceptions import AssetNotFound
from app.domain.ports.repository import IAssetRepository


class DisposeAssetUseCase:
    def __init__(self, asset_repository: IAssetRepository):
        self.asset_repository = asset_repository

    def execute(self, asset_id: UUID):
        """Mark an asset as disposed (idempotent — already-disposed assets are returned as-is)."""
        asset = self.asset_repository.find_by_id(str(asset_id))
        if not asset:
            raise AssetNotFound(f"Asset with id {asset_id} not found.")
        
        if not asset.disposed:
            asset.disposed = True
            asset.updated_at = datetime.now(timezone.utc)
            self.asset_repository.save(asset)
        
        return asset
