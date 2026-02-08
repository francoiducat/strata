"""
PortfolioSnapshot SQLAlchemy Model
"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base, generate_uuid

if TYPE_CHECKING:
    from .portfolio import PortfolioModel


class PortfolioSnapshotModel(Base):
    """
    Portfolio Snapshot - auto-calculated total value of all assets at a point in time
    """
    __tablename__ = "portfolio_snapshots"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    portfolio_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("portfolios.id"),
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
    portfolio: Mapped["PortfolioModel"] = relationship(
        "PortfolioModel",
        back_populates="snapshots"
    )

    def __repr__(self) -> str:
        return f"<PortfolioSnapshotModel(id={self.id}, portfolio_id={self.portfolio_id}, value={self.value})>"