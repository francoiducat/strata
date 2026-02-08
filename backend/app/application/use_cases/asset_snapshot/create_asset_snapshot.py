"""
Use Case: Create Asset Snapshot
"""
from datetime import datetime
from typing import Optional

from app.domain.entities.asset_snapshot import AssetSnapshot
from app.domain.exceptions import AssetNotFound
from app.domain.ports.repository import IAssetSnapshotRepository, IAssetRepository


class CreateAssetSnapshotUseCase:
    """Creates a snapshot for an asset."""

    def __init__(self, snapshot_repo: IAssetSnapshotRepository, asset_repo: IAssetRepository):
        self.snapshot_repo = snapshot_repo
        self.asset_repo = asset_repo

    def execute(self, asset_id: str, observed_at: Optional[datetime], value: float) -> AssetSnapshot:
        asset = self.asset_repo.find_by_id(asset_id)
        if not asset:
            raise AssetNotFound(f"Asset with id {asset_id} not found.")
        snapshot = AssetSnapshot(asset_id=asset_id, observed_at=observed_at or datetime.utcnow(), value=value)
        return self.snapshot_repo.save(snapshot)

