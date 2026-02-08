"""
Pydantic schemas for Asset API responses (GET).
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic.config import ConfigDict

from .shared_schemas import AssetTypeNestedResponse, PortfolioNestedResponse


class AssetResponse(BaseModel):
    id: UUID
    name: str
    quantity: Optional[Decimal] = None
    created_at: datetime
    updated_at: datetime
    asset_type: AssetTypeNestedResponse
    portfolio: PortfolioNestedResponse

    model_config = ConfigDict(from_attributes=True)
