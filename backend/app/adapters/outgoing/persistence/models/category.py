"""
Category SQLAlchemy Model
"""
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING

from .base import Base, generate_uuid

if TYPE_CHECKING:
    from .asset import AssetModel


class CategoryModel(Base):
    """
    Category - hierarchical, many-to-many organization for assets
    WordPress-style: assets can belong to multiple categories
    """
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    parent_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("categories.id"),
        nullable=True
    )

    # Relationships
    parent: Mapped[Optional["CategoryModel"]] = relationship(
        "CategoryModel",
        remote_side=[id],
        back_populates="children"
    )

    children: Mapped[list["CategoryModel"]] = relationship(
        "CategoryModel",
        back_populates="parent"
    )

    assets: Mapped[list["AssetModel"]] = relationship(
        "AssetModel",
        secondary="asset_categories",
        back_populates="categories"
    )

    def __repr__(self) -> str:
        return f"<CategoryModel(id={self.id}, name={self.name})>"