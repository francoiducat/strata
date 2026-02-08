"""
Tag SQLAlchemy Model
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base, generate_uuid

if TYPE_CHECKING:
    from .asset import AssetModel


class TagModel(Base):
    """
    Tag - flat labels for additional asset metadata
    Many-to-many with assets
    """
    __tablename__ = "tags"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    # Relationships
    assets: Mapped[list["AssetModel"]] = relationship(
        "AssetModel",
        secondary="asset_tags",
        back_populates="tags"
    )

    def __repr__(self) -> str:
        return f"<TagModel(id={self.id}, name={self.name})>"