"""
Shared Pydantic schemas used across multiple API responses.
"""
from uuid import UUID
from pydantic import BaseModel
from pydantic.config import ConfigDict


class AssetTypeNestedResponse(BaseModel):
    """Nested AssetType response (used in Asset responses)."""
    code: str
    label: str

    model_config = ConfigDict(from_attributes=True)


class PortfolioNestedResponse(BaseModel):
    """Nested Portfolio response (used in Asset responses)."""
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)
