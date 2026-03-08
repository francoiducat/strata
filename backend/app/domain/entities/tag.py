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

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Tag) and self.id == other.id