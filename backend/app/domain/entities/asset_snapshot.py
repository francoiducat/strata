"""
AssetSnapshot Domain Entity
"""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
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
    value: Decimal
    observed_at: datetime
    # Add a back-reference to the parent Asset to access portfolios-level info.
    # This field is excluded from serialization to prevent circular reference errors
    # and must be populated by the repository/mapper when constructing the entity.
    asset: "Asset" = Field(exclude=True, repr=False)

    model_config = ConfigDict(from_attributes=True)

    def get_currency(self) -> str:
        """
        Returns the currency of the snapshot, which is assumed to be the base
        currency of the portfolios the asset belongs to.
        """
        return self.asset.portfolio.base_currency