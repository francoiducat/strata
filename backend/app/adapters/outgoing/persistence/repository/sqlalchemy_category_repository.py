"""
SQLAlchemy Category Repository Implementation

Concrete implementation of CategoryRepository using SQLAlchemy.
"""
from typing import Optional, cast, Any
from sqlalchemy.orm import Session

from app.domain.ports.repository.category_repository import ICategoryRepository
from app.adapters.outgoing.persistence.models import CategoryModel


class SQLAlchemyCategoryRepository(ICategoryRepository):
    """
    SQLAlchemy implementation of CategoryRepository.

    Handles persistence operations for Category reference data.
    """

    def __init__(self, session: Session):
        """
        Initialize repository with persistence session.

        Args:
            session: SQLAlchemy session
        """
        self._session = session

    def save(self, entity: CategoryModel) -> CategoryModel:
        """Save or update a category and return the saved entity."""
        self._session.add(entity)
        self._session.flush()
        return entity

    def find_by_id(self, entity_id: str) -> Optional[CategoryModel]:
        """Find category by id."""
        return self._session.query(CategoryModel).filter(CategoryModel.id == entity_id).first()

    def find_all(self) -> list[CategoryModel]:
        """Return all categories."""
        return cast(list[CategoryModel], cast(Any, self._session.query(CategoryModel).all()))

    def delete(self, entity_id: str) -> bool:
        """Delete category by id."""
        obj = self.find_by_id(entity_id)
        if obj:
            self._session.delete(obj)
            self._session.flush()
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        """Check existence by id."""
        return self._session.query(
            self._session.query(CategoryModel).filter(CategoryModel.id == entity_id).exists()
        ).scalar()

    # Domain / interface-specific methods
    def find_by_name(self, name: str) -> Optional[CategoryModel]:
        """Find category by exact name."""
        return self._session.query(CategoryModel).filter(CategoryModel.name == name).first()

    def find_root_categories(self) -> list[CategoryModel]:
        """Find all root categories (no parent)."""
        return self._session.query(CategoryModel).filter(CategoryModel.parent_id == None).all()

    def find_children(self, parent_id: str) -> list[CategoryModel]:
        """Find all children of a category."""
        return self._session.query(CategoryModel).filter(CategoryModel.parent_id == parent_id).all()

    def count_assets(self, category_id: str) -> int:
        """Count number of assets by id."""
        from app.adapters.outgoing.persistence.models import AssetModel
        return self._session.query(AssetModel).join(
            AssetModel.categories
        ).filter(CategoryModel.id == category_id).count()
