"""
SQLAlchemy AssetType Repository Implementation

Concrete implementation of AssetTypeRepository using SQLAlchemy.
"""
from typing import Optional, cast, Any
from sqlalchemy.orm import Session

from app.domain.ports.repository.asset_type_repository import IAssetTypeRepository
from app.adapters.outgoing.persistence.models import AssetTypeModel


class SQLAlchemyAssetTypeRepository(IAssetTypeRepository):
    """
    SQLAlchemy implementation of AssetTypeRepository.

    Handles persistence operations for AssetType reference data.
    """

    def __init__(self, session: Session):
        """
        Initialize repository with persistence session.

        Args:
            session: SQLAlchemy session
        """
        self._session = session

    def save(self, entity: AssetTypeModel) -> AssetTypeModel:
        """
        Save (create or update) an asset type.

        Returns the saved entity after flush to populate DB-generated fields.
        """
        self._session.add(entity)
        self._session.flush()
        return entity

    def find_by_id(self, entity_id: str) -> Optional[AssetTypeModel]:
        """Find an AssetType by its id."""
        entity_id = str(entity_id)
        return self._session.query(AssetTypeModel).filter(AssetTypeModel.id == entity_id).first()

    def find_all(self) -> list[AssetTypeModel]:
        """Return all asset types."""
        return cast(list[AssetTypeModel], cast(Any, self._session.query(AssetTypeModel).all()))

    def delete(self, entity_id: str) -> bool:
        """Delete an asset type by id."""
        entity_id = str(entity_id)
        obj = self.find_by_id(entity_id)
        if obj:
            self._session.delete(obj)
            self._session.flush()
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        """Check existence by id."""
        entity_id = str(entity_id)
        return self._session.query(
            self._session.query(AssetTypeModel).filter(AssetTypeModel.id == entity_id).exists()
        ).scalar()

    # Domain / interface-specific methods
    def find_by_code(self, code: str) -> Optional[AssetTypeModel]:
        """Find an asset type by its code."""
        return self._session.query(AssetTypeModel).filter(AssetTypeModel.code == code).first()

    def find_all_codes(self) -> list[str]:
        """Return all asset type codes (useful for reference endpoints)."""
        rows = self._session.query(AssetTypeModel.code).all()
        return [r[0] for r in rows] if rows else []
