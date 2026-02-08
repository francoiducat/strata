"""
Portfolio Domain Entity
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
    from .portfolio_snapshot import PortfolioSnapshot


class Portfolio(BaseModel):
    """
    Portfolio domain entity. Represents the root aggregate for a user's assets.
    """
    id: UUID
    name: str
    base_currency: str
    assets: list[Asset] = Field(default_factory=list)
    snapshots: list[PortfolioSnapshot] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    def total_value(self, at: Optional[datetime] = None) -> Decimal:
        """
        Calculates the total value of the portfolios at a specific time by summing
        the values of all non-disposed assets.

        The value of each asset is determined by its most recent snapshot.
        """
        from decimal import Decimal as _Decimal
        from typing import cast

        total = sum(
            (asset.current_value(at=at) for asset in self.assets if not asset.disposed),
            _Decimal('0')
        )

        # Cast to Decimal for the typechecker (sum with start value is Decimal at runtime)
        return cast(Decimal, total)
