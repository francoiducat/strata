"""
Tag Domain Entity
"""
from __future__ import annotations
from uuid import UUID

from pydantic import BaseModel


class Tag(BaseModel):
    """
    Tag domain entity. Represents a flat label for asset metadata.
    """
    id: UUID
    name: str