"""
SQLAlchemy Asset Repository Implementation

Concrete implementation of AssetRepository using SQLAlchemy.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session, joinedload

from app.domain.ports.repository.asset_repository import IAssetRepository
from app.adapters.outgoing.persistence.models.asset import AssetModel
from app.adapters.outgoing.persistence.models import CategoryModel, TagModel


class SQLAlchemyAssetRepository(IAssetRepository):
    """
    SQLAlchemy implementation of AssetRepository.

    Handles persistence operations for Asset aggregates.
    """

    def __init__(self, session: Session):
        """
        Initialize repository with persistence session.

        Args:
            session: SQLAlchemy session
        """
        self._session = session

    def save(self, entity: AssetModel) -> AssetModel:
        """
        Save (create or update) an asset.

        Args:
            entity: Asset to save

        Returns:
            The saved Asset with DB-generated fields populated (after flush)
        """
        self._session.add(entity)
        self._session.flush()
        return entity

    def find_by_id(self, entity_id: str) -> Optional[AssetModel]:
        """
        Find asset by ID.

        Args:
            entity_id: UUID of asset

        Returns:
            Asset if found, None otherwise
        """
        return self._session.query(AssetModel).filter(AssetModel.id == entity_id).first()

    def find_all(self) -> list[AssetModel]:
        """
        Get all assets.

        Returns:
            list of all assets
        """
        return self._session.query(AssetModel).all()

    def delete(self, entity_id: str) -> bool:
        """
        Delete asset by ID.

        Args:
            entity_id: UUID of asset

        Returns:
            True if deleted, False if not found
        """
        asset = self.find_by_id(entity_id)
        if asset:
            self._session.delete(asset)
            self._session.flush()
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        """
        Check if an asset exists.

        Args:
            entity_id: UUID of asset

        Returns:
            True if exists, False otherwise
        """
        return self._session.query(
            self._session.query(AssetModel).filter(AssetModel.id == entity_id).exists()
        ).scalar()

    # Domain / interface-specific methods
    def find_by_portfolio(self, portfolio_id: str) -> list[AssetModel]: # type: ignore
        """Return assets belonging to a portfolios."""
        return self._session.query(AssetModel).filter(AssetModel.portfolio_id == portfolio_id).all()

    def find_by_type(self, asset_type_code: str) -> list[AssetModel]:
        """Return assets of a given asset type code."""
        return self._session.query(AssetModel).filter(AssetModel.type_id == asset_type_code).all()

    def find_by_category(self, category_id: str) -> list[AssetModel]:
        """Return assets with a specific category."""
        return self._session.query(AssetModel).join(AssetModel.categories).filter(CategoryModel.id == category_id).all()

    def find_by_tag(self, tag_id: str) -> list[AssetModel]:
        """Return assets with a specific tag."""
        return self._session.query(AssetModel).join(AssetModel.tags).filter(TagModel.id == tag_id).all()

    def find_active(self, portfolio_id: str) -> list[AssetModel]:
        """Return non-disposed assets in a portfolios."""
        return self._session.query(AssetModel).filter(
            AssetModel.portfolio_id == portfolio_id,
            AssetModel.disposed == False
        ).all()

    def find_disposed(self, portfolio_id: str) -> list[AssetModel]:
        """Return disposed assets in a portfolios."""
        return self._session.query(AssetModel).filter(
            AssetModel.portfolio_id == portfolio_id,
            AssetModel.disposed == True
        ).all()

    def find_with_snapshots(
            self,
            asset_id: str,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> Optional[AssetModel]:
        """Find asset with snapshots in date range."""
        from app.adapters.outgoing.persistence.models import AssetSnapshotModel

        asset = self.find_by_id(asset_id)

        if not asset:
            return None

        # Load snapshots with filters applied at the DB level.
        # This is more efficient than loading all snapshots and filtering in Python.
        snapshot_query = self._session.query(AssetSnapshotModel).filter(
            AssetSnapshotModel.asset_id == asset_id
        )
        if start_date:
            snapshot_query = snapshot_query.filter(AssetSnapshotModel.date >= start_date)
        if end_date:
            snapshot_query = snapshot_query.filter(AssetSnapshotModel.date <= end_date)

        asset.snapshots = snapshot_query.all() # type: ignore
        return asset

    def add_category(self, asset_id: str, category_id: str) -> bool:
        """Attach category to an asset (many-to-many)."""
        asset = self._session.query(AssetModel).options(joinedload(AssetModel.categories)).filter(AssetModel.id == asset_id).first()
        if asset:
            # Avoid re-adding if the relationship already exists
            category_ids = {c.id for c in asset.categories}
            if category_id in category_ids:
                return True  # Already associated

            category = self._session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
            if category:
                asset.categories.append(category)
                self._session.flush()
                return True
        return False

    def remove_category(self, asset_id: str, category_id: str) -> bool:
        """Remove category from an asset (many-to-many)."""
        asset = self._session.query(AssetModel).options(joinedload(AssetModel.categories)).filter(AssetModel.id == asset_id).first()
        if asset:
            category_to_remove = next((c for c in asset.categories if c.id == category_id), None)
            if category_to_remove:
                asset.categories.remove(category_to_remove)
                self._session.flush()
                return True
        return False

    def add_tag(self, asset_id: str, tag_id: str) -> bool:
        """Add a tag to an asset."""
        asset = self._session.query(AssetModel).options(joinedload(AssetModel.tags)).filter(AssetModel.id == asset_id).first()
        if asset:
            # Avoid re-adding if the relationship already exists
            if tag_id not in {t.id for t in asset.tags}:
                tag = self._session.query(TagModel).filter(TagModel.id == tag_id).first()
                if not tag:
                    return False # Tag not found
                asset.tags.append(tag)
                self._session.flush()
            return True
        return False

    def remove_tag(self, asset_id: str, tag_id: str) -> bool:
        """Remove a tag from an asset."""
        asset = self._session.query(AssetModel).options(joinedload(AssetModel.tags)).filter(AssetModel.id == asset_id).first()
        if asset:
            tag_to_remove = next((t for t in asset.tags if t.id == tag_id), None)
            if tag_to_remove:
                asset.tags.remove(tag_to_remove)
                self._session.flush()
                return True
        return False
