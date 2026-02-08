"""
Asset SQLAlchemy Model
"""
from decimal import Decimal
from sqlalchemy import String, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING

from .base import Base, TimestampMixin, AuditMixin, generate_uuid

if TYPE_CHECKING:
    from .portfolio import PortfolioModel
    from .asset_type import AssetTypeModel
    from .transaction import TransactionModel
    from .asset_snapshot import AssetSnapshotModel
    from .category import CategoryModel
    from .tag import TagModel


class AssetModel(Base, TimestampMixin, AuditMixin):
    """
    Asset - anything you own (stocks, real estate, LEGO, clothes, etc.)
    """
    __tablename__ = "assets"  # The table name remains 'assets'

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

    asset_type_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("asset_types.id"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    quantity: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(20, 8),
        nullable=True
    )

    disposed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True
    )

    # Relationships
    portfolio: Mapped["PortfolioModel"] = relationship(
        "PortfolioModel",
        back_populates="assets"
    )

    asset_type: Mapped["AssetTypeModel"] = relationship(
        "AssetTypeModel",
        back_populates="assets"
    )

    transactions: Mapped[list["TransactionModel"]] = relationship(
        "TransactionModel",
        back_populates="asset",
        cascade="all, delete-orphan",
        order_by="TransactionModel.occurred_at.desc()"
    )

    snapshots: Mapped[list["AssetSnapshotModel"]] = relationship(
        "AssetSnapshotModel",
        back_populates="asset",
        cascade="all, delete-orphan",
        order_by="AssetSnapshotModel.observed_at.desc()"
    )

    categories: Mapped[list["CategoryModel"]] = relationship(
        "CategoryModel",
        secondary="asset_categories",
        back_populates="assets"
    )

    tags: Mapped[list["TagModel"]] = relationship(
        "TagModel",
        secondary="asset_tags",
        back_populates="assets"
    )

    def __repr__(self) -> str:
        return f"<AssetModel(id={self.id}, name={self.name}, type={self.asset_type.code if self.asset_type else None})>"