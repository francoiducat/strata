"""
AssetSnapshot Domain Entity
"""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

if TYPE_CHECKING:
    from .asset import Asset

class AssetSnapshot(BaseModel):
    """
    AssetSnapshot domain entity. Represents the value of an asset at a point in time.
    """
    id: UUID
    asset_id: UUID
    value: Decimal
    observed_at: datetime
    # Optional back-reference to parent Asset for cross-aggregate business logic.
    # Excluded from serialization; populated by the repository mapper when needed.
    asset: Optional["Asset"] = Field(default=None, exclude=True, repr=False)

    model_config = ConfigDict(from_attributes=True)

    def get_currency(self) -> str:
        """
        Returns the currency of the snapshot. Requires `asset` back-reference to be loaded.
        """
        if self.asset is None:
            raise ValueError("Asset back-reference is not loaded on this snapshot.")
        return self.asset.portfolio.base_currency