"""
PortfolioSnapshot Domain Entity
"""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

if TYPE_CHECKING:
    from .portfolio import Portfolio

class PortfolioSnapshot(BaseModel):
    """
    PortfolioSnapshot domain entity. Represents the total calculated value of a
    portfolios at a point in time.
    """
    id: UUID
    portfolio_id: UUID
    value: Decimal
    observed_at: datetime
    # Optional back-reference to parent Portfolio for cross-aggregate business logic.
    # Excluded from serialization; populated by the repository mapper when needed.
    portfolio: Optional["Portfolio"] = Field(default=None, exclude=True, repr=False)

    model_config = ConfigDict(from_attributes=True)

    def get_currency(self) -> str:
        """
        Returns the currency of the snapshot. Requires `portfolio` back-reference to be loaded.
        """
        if self.portfolio is None:
            raise ValueError("Portfolio back-reference is not loaded on this snapshot.")
        return self.portfolio.base_currency