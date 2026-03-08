"""Use Case: Get Asset Snapshots"""
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from app.domain.exceptions import AssetNotFound
from app.domain.ports.repository import IAssetSnapshotRepository, IAssetRepository


class GetAssetSnapshotsUseCase:
    def __init__(self, snapshot_repo: IAssetSnapshotRepository, asset_repo: IAssetRepository):
        self.snapshot_repo = snapshot_repo
        self.asset_repo = asset_repo

    def execute(
        self,
        asset_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List:
        asset = self.asset_repo.find_by_id(str(asset_id))
        if not asset:
            raise AssetNotFound(f"Asset with id {asset_id} not found.")
        return self.snapshot_repo.get_snapshots(str(asset_id), start_date, end_date)
