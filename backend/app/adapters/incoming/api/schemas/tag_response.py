"""Pydantic schema for Tag API response."""
from uuid import UUID
from pydantic import BaseModel
from pydantic.config import ConfigDict


class TagResponse(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)
