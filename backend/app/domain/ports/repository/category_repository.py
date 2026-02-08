"""
Category Repository Interface (Port)

Defines operations for Category (hierarchical taxonomy)
"""
from abc import abstractmethod
from typing import Optional, List
from uuid import UUID

from .base_repository import BaseRepository
from ....domain.entities.category import Category


class ICategoryRepository(BaseRepository[Category]):
    """
    Repository interface for Category
    """

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Category]:
        """
        Find category by exact name

        Args:
            name: Category name (unique)

        Returns:
            Category if found, None otherwise
        """
        pass

    @abstractmethod
    def find_root_categories(self) -> List[Category]:
        """
        Find all root categories (no parent)

        Returns:
            List of root categories
        """
        pass

    @abstractmethod
    def find_children(self, parent_id: UUID) -> List[Category]:
        """
        Find all direct children of a category

        Args:
            parent_id: UUID of parent category

        Returns:
            List of child categories
        """
        pass

    @abstractmethod
    def count_assets(self, category_id: UUID) -> int:
        """
        Count assets in this category

        Args:
            category_id: UUID of category

        Returns:
            Number of assets
        """
        pass