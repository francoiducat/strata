"""Pydantic schemas for Tag API requests."""
from uuid import UUID
from pydantic import BaseModel


class TagCreateRequest(BaseModel):
    name: str


class AssetTagAssignRequest(BaseModel):
    """Request body for assigning a tag to an asset."""
    tag_id: UUID
