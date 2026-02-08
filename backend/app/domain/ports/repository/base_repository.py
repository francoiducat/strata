"""
Base Repository Interface

Generic repository pattern for all entities
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from uuid import UUID

# Generic type for entity
T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository defining common CRUD operations

    All repositories should inherit from this and implement these methods.
    """

    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Save (create or update) an entity

        Args:
            entity: Entity to save

        Returns:
            Saved entity with any generated fields populated
        """
        pass

    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[T]:
        """
        Find entity by ID

        Args:
            entity_id: UUID of entity

        Returns:
            Entity if found, None otherwise
        """
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        """
        Get all entities

        Returns:
            List of all entities (may be empty)
        """
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Delete entity by ID

        Args:
            entity_id: UUID of entity to delete

        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    def exists(self, entity_id: str) -> bool:
        """
        Check if entity exists

        Args:
            entity_id: UUID of entity

        Returns:
            True if exists, False otherwise
        """
        pass