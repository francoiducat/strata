"""
Category Domain Entity
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

if TYPE_CHECKING:
    from .asset import Asset


class Category(BaseModel):
    """
    Category domain entity. Represents a hierarchical, many-to-many organization
    for assets.
    """
    id: UUID
    name: str
    parent: Optional[Category] = None
    # The following fields must be populated by the repository/mapper.
    # They are excluded from serialization to prevent circular reference errors.
    children: List["Category"] = Field(default_factory=list, exclude=True, repr=False)
    assets: List["Asset"] = Field(default_factory=list, exclude=True, repr=False)

    model_config = ConfigDict(from_attributes=True)

    def get_hierarchy(self) -> List[Category]:
        """
        Returns the hierarchical path from the current category up to the root.
        Example: [current_category, parent_category, root_category]
        """
        hierarchy = []
        current: Optional[Category] = self
        while current:
            hierarchy.append(current)
            current = current.parent
        return hierarchy

    def get_all_assets(self) -> List[Asset]:
        """
        Returns a list of all unique assets in this category and all its
        sub-categories.

        Note: This requires the 'children' and 'assets' fields to be populated
        by the repository when the category is fetched.
        """
        # Use a dictionary to store unique assets by ID to prevent duplicates
        unique_assets: dict[UUID, Asset] = {asset.id: asset for asset in self.assets}

        for child in self.children:
            # Recursively get assets from child categories
            for asset in child.get_all_assets():
                unique_assets[asset.id] = asset  # Add if not present

        return list(unique_assets.values())