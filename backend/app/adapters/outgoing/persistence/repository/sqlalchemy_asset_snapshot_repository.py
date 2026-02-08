"""
SQLAlchemy AssetSnapshot Repository Implementation

Concrete implementation of AssetSnapshotRepository using SQLAlchemy.
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.domain.ports.repository.asset_snapshot_repository import IAssetSnapshotRepository
from app.adapters.outgoing.persistence.models import AssetSnapshotModel


class SQLAlchemyAssetSnapshotRepository(IAssetSnapshotRepository):
    """
    SQLAlchemy implementation of AssetSnapshotRepository.
    """

    def __init__(self, session: Session):
        """Initialize repository with persistence session."""
        self._session = session

    # CRUD core methods (implementations of common abstract methods)
    def save(self, entity: AssetSnapshotModel) -> AssetSnapshotModel:
        """Persist an asset snapshot and return the saved entity."""
        self._session.add(entity)
        self._session.flush()
        return entity

    def find_by_id(self, entity_id: str) -> Optional[AssetSnapshotModel]:
        """Find snapshot by id."""
        return self._session.query(AssetSnapshotModel).filter(AssetSnapshotModel.id == entity_id).first()

    def find_all(self) -> list[AssetSnapshotModel]:
        """Return all asset snapshots."""
        from typing import cast, Any
        return cast(List[AssetSnapshotModel], cast(Any, self._session.query(AssetSnapshotModel).all()))

    def delete(self, entity_id: str) -> bool:
        """Delete asset snapshot by id."""
        obj = self.find_by_id(entity_id)
        if obj:
            self._session.delete(obj)
            self._session.flush()
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        """Check existence by id."""
        return self._session.query(
            self._session.query(AssetSnapshotModel).filter(AssetSnapshotModel.id == entity_id).exists()
        ).scalar()


    # Domain / interface-specific methods
    def get_snapshots(self, asset_id: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> list[AssetSnapshotModel]:
        """Retrieve snapshots for an asset optionally filtered by date range."""
        q = self._session.query(AssetSnapshotModel).filter(AssetSnapshotModel.asset_id == asset_id)
        if start_date:
            q = q.filter(AssetSnapshotModel.observed_at >= start_date)
        if end_date:
            q = q.filter(AssetSnapshotModel.observed_at <= end_date)
        from typing import cast, Any
        return cast(List[AssetSnapshotModel], cast(Any, q.all()))

    def get_latest_snapshot(self, asset_id: str) -> Optional[AssetSnapshotModel]:
        """Return the latest snapshot for an asset or None."""
        return self._session.query(AssetSnapshotModel).filter(
            AssetSnapshotModel.asset_id == asset_id
        ).order_by(AssetSnapshotModel.observed_at.desc()).first()
