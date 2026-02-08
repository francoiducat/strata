"""
AssetSnapshot SQLAlchemy Model
"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base, generate_uuid

if TYPE_CHECKING:
    from .asset import AssetModel


class AssetSnapshotModel(Base):
    """
    Asset Snapshot - manually entered value of an asset at a point in time
    """
    __tablename__ = "asset_snapshots"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    asset_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("assets.id"),
        nullable=False,
        index=True
    )

    value: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False
    )

    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    # Relationships
    asset: Mapped["AssetModel"] = relationship(
        "AssetModel",
        back_populates="snapshots"
    )

    def __repr__(self) -> str:
        return f"<AssetSnapshotModel(id={self.id}, asset_id={self.asset_id}, value={self.value})>"