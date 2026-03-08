"""Pydantic schema for AssetType API response."""
from uuid import UUID
from pydantic import BaseModel
from pydantic.config import ConfigDict


class AssetTypeResponse(BaseModel):
    id: UUID
    code: str
    label: str

    model_config = ConfigDict(from_attributes=True)
