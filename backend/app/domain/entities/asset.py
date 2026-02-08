"""
Asset Domain Entity
"""
from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, Set, TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

if TYPE_CHECKING:
    from .asset_snapshot import AssetSnapshot
    from .asset_type import AssetType
    from .category import Category
    from .portfolio import Portfolio
    from .tag import Tag
    from .transaction import Transaction


class Asset(BaseModel):
    """
    Asset domain entity. Represents anything of value that is tracked.
    This is a behavior-oriented model, part of the domain core, and is
    framework-agnostic. It contains business logic and rules.
    """
    id: UUID
    name: str
    asset_type: "AssetType"
    portfolio: "Portfolio"
    quantity: Optional[Decimal] = None
    disposed: bool = False

    categories: Set["Category"] = Field(default_factory=set)
    tags: Set["Tag"] = Field(default_factory=set)
    transactions: list["Transaction"] = Field(default_factory=list)
    snapshots: list["AssetSnapshot"] = Field(default_factory=list)

    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str

    model_config = ConfigDict(from_attributes=True)

    # Business logic methods from the conceptual model
    def current_value(self, at: Optional[datetime] = None) -> Decimal:
        """
        Calculates the value of the asset at a specific time.
        For simplicity, it uses the most recent snapshot if available.
        """
        if not self.snapshots:
            return Decimal("0.0")

        # Assumes snapshots are pre-sorted descending by date from the repository
        relevant_snapshot = self.snapshots[0]
        if at:
            # Find the latest snapshot before or at the given date
            for snapshot in self.snapshots:
                if snapshot.observed_at <= at:
                    relevant_snapshot = snapshot
                    break

        return relevant_snapshot.value

    def dispose(self, at: Optional[datetime] = None) -> None:
        """Marks the asset as disposed."""
        self.disposed = True
        self.updated_at = at or datetime.now(timezone.utc)

    def add_category(self, category: "Category") -> None:
        """Adds a category to the asset's collection."""
        self.categories.add(category)

    def remove_category(self, category: "Category") -> None:
        """Removes a category from the asset's collection."""
        self.categories.discard(category)