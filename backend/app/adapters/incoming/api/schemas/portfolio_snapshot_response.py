"""
Pydantic schemas for PortfolioSnapshot API responses.
"""
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from pydantic.config import ConfigDict


class PortfolioSnapshotResponse(BaseModel):
    id: UUID
    portfolio_id: UUID
    value: Decimal
    observed_at: datetime

    model_config = ConfigDict(from_attributes=True)
