"""
Transaction SQLAlchemy Model
"""
from datetime import datetime
from decimal import Decimal

from annotated_types import Timezone
from sqlalchemy import String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base, generate_uuid

if TYPE_CHECKING:
    from .asset import AssetModel


class TransactionModel(Base):
    """
    Transaction - records of asset acquisitions, disposals, and adjustments
    Types: ACQUIRE, DISPOSE, ADJUST
    """
    __tablename__ = "transactions"

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

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(20, 8),
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    # Relationships
    asset: Mapped["AssetModel"] = relationship(
        "AssetModel",
        back_populates="transactions"
    )

    def __repr__(self) -> str:
        return f"<TransactionModel(id={self.id}, type={self.type}, asset_id={self.asset_id})>"