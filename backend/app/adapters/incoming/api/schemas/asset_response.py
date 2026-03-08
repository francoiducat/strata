"""
Pydantic schemas for Asset API responses (GET).
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic.config import ConfigDict

from .shared_schemas import AssetTypeNestedResponse, PortfolioNestedResponse
from .tag_response import TagResponse
from .category_response import CategoryResponse


class AssetResponse(BaseModel):
    id: UUID
    name: str
    disposed: bool = False
    quantity: Optional[Decimal] = None
    created_at: datetime
    updated_at: datetime
    asset_type: AssetTypeNestedResponse
    portfolio: PortfolioNestedResponse
    tags: List[TagResponse] = []
    categories: List[CategoryResponse] = []

    model_config = ConfigDict(from_attributes=True)
