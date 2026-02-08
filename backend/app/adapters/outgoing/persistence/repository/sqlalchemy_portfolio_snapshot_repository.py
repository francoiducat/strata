"""
SQLAlchemy PortfolioSnapshot Repository Implementation

Concrete implementation of PortfolioSnapshotRepository using SQLAlchemy.
"""
from typing import Optional, cast
from datetime import datetime
from sqlalchemy.orm import Session

from app.domain.ports.repository.portfolio_snapshot_repository import IPortfolioSnapshotRepository
from app.adapters.outgoing.persistence.models import PortfolioSnapshotModel


class SQLAlchemyPortfolioSnapshotRepository(IPortfolioSnapshotRepository):
    """
    SQLAlchemy implementation of PortfolioSnapshotRepository.
    """

    def __init__(self, session: Session):
        """Initialize repository with persistence session."""
        self._session = session

    def save(self, entity: PortfolioSnapshotModel) -> PortfolioSnapshotModel:
        """Persist a portfolios snapshot and return the saved entity."""
        self._session.add(entity)
        self._session.flush()
        return entity

    def find_by_id(self, entity_id: str) -> Optional[PortfolioSnapshotModel]:
        """Find snapshot by id."""
        return self._session.query(PortfolioSnapshotModel).filter(PortfolioSnapshotModel.id == entity_id).first()

    def find_all(self) -> list[PortfolioSnapshotModel]:
        """Return all portfolios snapshots."""
        return cast(list[PortfolioSnapshotModel], self._session.query(PortfolioSnapshotModel).all())

    def delete(self, entity_id: str) -> bool:
        """Delete snapshot by id."""
        obj = self.find_by_id(entity_id)
        if obj:
            self._session.delete(obj)
            self._session.flush()
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        """Check snapshot existence by id."""
        return self._session.query(
            self._session.query(PortfolioSnapshotModel).filter(PortfolioSnapshotModel.id == entity_id).exists()
        ).scalar()

    # Domain / interface-specific methods (keep in same order as the port)
    def get_snapshots(self, portfolio_id: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> list[PortfolioSnapshotModel]:
        """Retrieve snapshots for a portfolios optionally filtered by date range."""
        q = self._session.query(PortfolioSnapshotModel).filter(PortfolioSnapshotModel.portfolio_id == portfolio_id)
        if start_date:
            q = q.filter(PortfolioSnapshotModel.observed_at >= start_date)
        if end_date:
            q = q.filter(PortfolioSnapshotModel.observed_at <= end_date)
        return cast(list[PortfolioSnapshotModel], q.all())

    def get_latest_snapshot(self, portfolio_id: str) -> Optional[PortfolioSnapshotModel]:
        """Return the latest snapshot for a portfolios or None."""
        return self._session.query(PortfolioSnapshotModel).filter(
            PortfolioSnapshotModel.portfolio_id == portfolio_id
        ).order_by(PortfolioSnapshotModel.observed_at.desc()).first()
