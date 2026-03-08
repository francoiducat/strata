"""Pydantic schema for Category API response."""
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from pydantic.config import ConfigDict


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    parent_id: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)
