"""
Tag Repository Interface (Port)

Defines operations for Tag entities (simple lookup and association helpers).
"""
from abc import abstractmethod
from typing import Optional, List
from uuid import UUID

from .base_repository import BaseRepository
from ....domain.entities.tag import Tag


class ITagRepository(BaseRepository[Tag]):
    """
    Repository interface for Tag objects.
    """

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Tag]:
        """
        Find a tag by its exact name.

        Args:
            name: Tag name (unique)

        Returns:
            Tag if found, None otherwise
        """
        pass

    @abstractmethod
    def find_all(self) -> List[Tag]:
        """
        Return all tags.

        Returns:
            List of tags (may be empty)
        """
        pass

    @abstractmethod
    def find_by_asset(self, asset_id: UUID) -> List[Tag]:
        """
        Return all tags attached to a given asset.

        Args:
            asset_id: UUID of asset

        Returns:
            List of tags
        """
        pass

    @abstractmethod
    def attach_to_asset(self, asset_id: UUID, tag_id: UUID) -> bool:
        """
        Attach an existing tag to an asset.

        Args:
            asset_id: UUID of asset
            tag_id: UUID of tag

        Returns:
            True if attached, False otherwise
        """
        pass

    @abstractmethod
    def detach_from_asset(self, asset_id: UUID, tag_id: UUID) -> bool:
        """
        Remove a tag from an asset.

        Args:
            asset_id: UUID of asset
            tag_id: UUID of tag

        Returns:
            True if removed, False otherwise
        """
        pass
