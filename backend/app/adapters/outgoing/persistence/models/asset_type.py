"""
AssetType SQLAlchemy Model
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base, TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from .asset import AssetModel


class AssetTypeModel(Base, TimestampMixin):
    """
    Asset Type - controlled vocabulary for asset classification
    Examples: CASH, REAL_ESTATE, STOCKS, PERSONAL_PROPERTY, LOAN, etc.
    """
    __tablename__ = "asset_types"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    label: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Relationships
    assets: Mapped[list["AssetModel"]] = relationship(
        "AssetModel",
        back_populates="asset_type"
    )

    def __repr__(self) -> str:
        return f"<AssetTypeModel(code={self.code}, label={self.label})>"