"""Use Case: Create Asset Snapshot"""
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import uuid4
from app.domain.entities.asset_snapshot import AssetSnapshot
from app.domain.exceptions import AssetNotFound
from app.domain.ports.repository import IAssetSnapshotRepository, IAssetRepository


class CreateAssetSnapshotUseCase:
    """Creates a snapshot for an asset."""

    def __init__(self, snapshot_repo: IAssetSnapshotRepository, asset_repo: IAssetRepository):
        self.snapshot_repo = snapshot_repo
        self.asset_repo = asset_repo

    def execute(self, asset_id: str, value: Decimal, observed_at: Optional[datetime] = None) -> AssetSnapshot:
        asset = self.asset_repo.find_by_id(str(asset_id))
        if not asset:
            raise AssetNotFound(f"Asset with id {asset_id} not found.")

        snapshot = AssetSnapshot(
            id=uuid4(),
            asset_id=asset.id,
            value=value,
            observed_at=observed_at or datetime.now(timezone.utc),
        )
        return self.snapshot_repo.save(snapshot)
