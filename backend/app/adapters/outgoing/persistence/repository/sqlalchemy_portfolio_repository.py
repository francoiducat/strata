"""
SQLAlchemy Portfolio Repository Implementation

Concrete implementation of PortfolioRepository using SQLAlchemy
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload

from app.domain.ports.repository.portfolio_repository import IPortfolioRepository
from app.adapters.outgoing.persistence.models import PortfolioModel


class SQLAlchemyPortfolioRepository(IPortfolioRepository):
    """
    SQLAlchemy implementation of PortfolioRepository

    Handles persistence of Portfolio aggregates
    """

    def __init__(self, session: Session):
        """
        Initialize repository with persistence session

        Args:
            session: SQLAlchemy session
        """
        self._session = session

    def save(self, entity: PortfolioModel) -> PortfolioModel:
        """
        Save (create or update) a portfolios

        Args:
            entity: Portfolio to save

        Returns:
            Saved portfolios
        """
        self._session.add(entity)
        # Commit so the data is persisted across separate sessions/requests
        self._session.commit()
        # Refresh the instance to load generated fields (ids, timestamps)
        self._session.refresh(entity)
        return entity

    def find_by_id(self, entity_id: str) -> Optional[PortfolioModel]:
        """
        Find portfolios by ID

        Args:
            entity_id: UUID of portfolios

        Returns:
            Portfolio if found, None otherwise
        """
        entity_id = str(entity_id)
        return self._session.query(PortfolioModel).filter(
            PortfolioModel.id == entity_id
        ).first()

    def find_all(self) -> list[PortfolioModel]:
        """
        Get all portfolios

        Returns:
            List of all portfolios
        """
        return self._session.query(PortfolioModel).all()

    def delete(self, entity_id: str) -> bool:
        """
        Delete portfolios by ID

        Args:
            entity_id: UUID of portfolios

        Returns:
            True if deleted, False if not found
        """
        portfolio = self.find_by_id(entity_id)
        if portfolio:
            self._session.delete(portfolio)
            self._session.commit()
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        """
        Check if portfolios exists

        Args:
            entity_id: UUID of portfolios

        Returns:
            True if exists, False otherwise
        """
        entity_id = str(entity_id)
        return self._session.query(
            self._session.query(PortfolioModel).filter(
                PortfolioModel.id == entity_id
            ).exists()
        ).scalar()

    def find_by_name(self, name: str) -> Optional[PortfolioModel]:
        """
        Find portfolios by exact name

        Args:
            name: Portfolio name

        Returns:
            Portfolio if found, None otherwise
        """
        return self._session.query(PortfolioModel).filter(
            PortfolioModel.name == name
        ).first()

    def find_with_assets(self, portfolio_id: str) -> Optional[PortfolioModel]:
        """
        Find portfolios with all its assets eagerly loaded

        Args:
            portfolio_id: UUID of portfolios

        Returns:
            Portfolio with assets loaded, None if not found
        """
        portfolio_id = str(portfolio_id)
        return self._session.query(PortfolioModel).options(
            joinedload(PortfolioModel.assets)
        ).filter(
            PortfolioModel.id == portfolio_id
        ).first()

    def find_with_snapshots(
        self,
        portfolio_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Optional[PortfolioModel]:
        """
        Find portfolios with snapshots in date range

        Args:
            portfolio_id: UUID of portfolios
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            Portfolio with filtered snapshots, None if not found
        """
        from app.adapters.outgoing.persistence.models import PortfolioSnapshotModel

        portfolio = self.find_by_id(portfolio_id)

        if not portfolio:
            return None

        # Load snapshots separately with filters applied at the DB level
        snapshot_query = self._session.query(PortfolioSnapshotModel).filter(
            PortfolioSnapshotModel.portfolio_id == portfolio_id
        )
        if start_date:
            snapshot_query = snapshot_query.filter(PortfolioSnapshotModel.observed_at >= start_date)
        if end_date:
            snapshot_query = snapshot_query.filter(PortfolioSnapshotModel.observed_at <= end_date)

        portfolio.snapshots = snapshot_query.order_by(PortfolioSnapshotModel.observed_at.desc()).all() # type: ignore
        return portfolio

    def count_assets(self, portfolio_id: str) -> int:
        """
        Count total assets in portfolios

        Args:
            portfolio_id: UUID of portfolios

        Returns:
            Number of assets (0 if portfolios not found)
        """
        from app.adapters.outgoing.persistence.models import AssetModel

        portfolio_id = str(portfolio_id)
        return self._session.query(AssetModel).filter(
            AssetModel.portfolio_id == portfolio_id
        ).count()