"""Pydantic schemas for Category API requests."""
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class CategoryCreateRequest(BaseModel):
    name: str
    parent_id: Optional[UUID] = None


class AssetCategoryAssignRequest(BaseModel):
    """Request body for assigning a category to an asset."""
    category_id: UUID


class CategoryAssetAssignRequest(BaseModel):
    """Request body for assigning an asset to a category."""
    asset_id: UUID
