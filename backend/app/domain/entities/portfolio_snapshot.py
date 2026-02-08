"""
PortfolioSnapshot Domain Entity
"""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
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
    value: Decimal
    observed_at: datetime
    # Add a back-reference to the parent Portfolio to access its base currency.
    # This field is excluded from serialization to prevent circular reference errors
    # and must be populated by the repository/mapper when constructing the entity.
    portfolio: "Portfolio" = Field(exclude=True, repr=False)

    model_config = ConfigDict(from_attributes=True)

    def get_currency(self) -> str:
        """
        Returns the currency of the snapshot, which is the base currency of the
        portfolios.
        """
        return self.portfolio.base_currency