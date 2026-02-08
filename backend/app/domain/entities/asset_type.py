"""
AssetType Domain Entity
"""
from __future__ import annotations
from uuid import UUID

from pydantic import BaseModel
from pydantic.config import ConfigDict


class AssetType(BaseModel):
    """
    AssetType domain entity. Represents a broad accounting classification.
    """
    id: UUID
    code: str
    label: str

    model_config = ConfigDict(from_attributes=True)
