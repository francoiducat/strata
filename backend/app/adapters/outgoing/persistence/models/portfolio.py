"""
Portfolio SQLAlchemy Model
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base, TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from .asset import AssetModel
    from .portfolio_snapshot import PortfolioSnapshotModel


class PortfolioModel(Base, TimestampMixin):
    """
    Portfolio entity - container for all user's assets
    """
    __tablename__ = "portfolios"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    base_currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="EUR"
    )

    # Relationships
    assets: Mapped[list["AssetModel"]] = relationship(
        "AssetModel",
        back_populates="portfolio",
        cascade="all, delete-orphan"
    )

    snapshots: Mapped[list["PortfolioSnapshotModel"]] = relationship(
        "PortfolioSnapshotModel",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        order_by="PortfolioSnapshotModel.observed_at.desc()"
    )

    def __repr__(self) -> str:
        return f"<PortfolioModel(id={self.id}, name={self.name}, currency={self.base_currency})>"