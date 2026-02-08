"""
Pydantic schemas for Asset API requests (POST, PUT).
"""
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class AssetCreateRequest(BaseModel):
    """Schema for creating a new asset."""
    portfolio_id: UUID
    asset_type_id: UUID
    name: str
    quantity: Optional[Decimal] = None
    created_by: str


class AssetUpdateRequest(BaseModel):
    """Schema for updating an existing asset."""
    name: str
    quantity: Optional[Decimal] = None
    updated_by: str


class AssetBulkCreateRequest(BaseModel):
    """Schema for creating multiple assets in a single request."""
    assets: List[AssetCreateRequest]