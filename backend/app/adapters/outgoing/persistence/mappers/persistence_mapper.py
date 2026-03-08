"""
PersistenceMapper

Bidirectional mapping between SQLAlchemy ORM models and domain entities.

Rules:
- ORM models never leave this layer (only domain entities are returned from repositories)
- Domain entities never depend on SQLAlchemy; this module is the only bridge
- Monetary amounts use 2 decimal places; asset quantities use 8 (crypto precision)
"""
from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from app.domain.entities.asset import Asset
from app.domain.entities.asset_snapshot import AssetSnapshot
from app.domain.entities.asset_type import AssetType
from app.domain.entities.category import Category
from app.domain.entities.portfolio import Portfolio
from app.domain.entities.portfolio_snapshot import PortfolioSnapshot
from app.domain.entities.tag import Tag

if TYPE_CHECKING:
    from app.adapters.outgoing.persistence.models.asset import AssetModel
    from app.adapters.outgoing.persistence.models.asset_snapshot import AssetSnapshotModel
    from app.adapters.outgoing.persistence.models.asset_type import AssetTypeModel
    from app.adapters.outgoing.persistence.models.category import CategoryModel
    from app.adapters.outgoing.persistence.models.portfolio import PortfolioModel
    from app.adapters.outgoing.persistence.models.portfolio_snapshot import PortfolioSnapshotModel
    from app.adapters.outgoing.persistence.models.tag import TagModel


class PersistenceMapper:
    """Static bidirectional ORM↔domain mapper."""

    # ------------------------------------------------------------------
    # ORM → Domain (simple entities)
    # ------------------------------------------------------------------

    @staticmethod
    def tag_to_domain(model: "TagModel") -> Tag:
        return Tag(id=UUID(model.id), name=model.name)

    @staticmethod
    def asset_type_to_domain(model: "AssetTypeModel") -> AssetType:
        return AssetType(id=UUID(model.id), code=model.code, label=model.label)

    @staticmethod
    def category_to_domain(model: "CategoryModel") -> Category:
        """Shallow mapping — parent is included if the relationship is already loaded."""
        parent: Category | None = None
        if model.parent is not None:
            parent = PersistenceMapper.category_to_domain(model.parent)
        return Category(id=UUID(model.id), name=model.name, parent=parent)

    # ------------------------------------------------------------------
    # ORM → Domain (aggregate root: Portfolio + Asset, breaks circular ref)
    # ------------------------------------------------------------------

    @staticmethod
    def _asset_with_portfolio(
        model: "AssetModel",
        portfolio: Portfolio,
        load_snapshots: bool = False,
    ) -> Asset:
        """
        Build an Asset domain entity using a pre-constructed Portfolio to avoid
        the circular Portfolio → assets → Asset → portfolio → Portfolio loop.
        """
        asset = Asset(
            id=UUID(model.id),
            name=model.name,
            portfolio=portfolio,
            asset_type=PersistenceMapper.asset_type_to_domain(model.asset_type),
            quantity=model.quantity,
            disposed=model.disposed,
            tags=set(PersistenceMapper.tag_to_domain(t) for t in (model.tags or [])),
            categories=set(PersistenceMapper.category_to_domain(c) for c in (model.categories or [])),
            created_at=model.created_at,
            updated_at=model.updated_at,
            created_by=model.created_by,
            updated_by=model.updated_by,
        )
        if load_snapshots and model.snapshots:
            asset.snapshots = [
                PersistenceMapper.asset_snapshot_to_domain(s)
                for s in model.snapshots
            ]
        return asset

    @staticmethod
    def asset_to_domain(model: "AssetModel", load_snapshots: bool = False) -> Asset:
        """
        Map AssetModel → Asset domain entity.
        Requires model.portfolio and model.asset_type to be eagerly loaded.
        """
        portfolio = PersistenceMapper.portfolio_to_domain(model.portfolio)
        return PersistenceMapper._asset_with_portfolio(model, portfolio, load_snapshots)

    @staticmethod
    def portfolio_to_domain(model: "PortfolioModel", load_assets: bool = False) -> Portfolio:
        """
        Map PortfolioModel → Portfolio domain entity.
        When load_assets=True, also maps nested assets (with their snapshots).
        Requires model.assets and model.assets[i].asset_type to be eagerly loaded
        when load_assets=True.
        """
        portfolio = Portfolio(
            id=UUID(model.id),
            name=model.name,
            base_currency=model.base_currency,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        if load_assets and model.assets:
            portfolio.assets = [
                PersistenceMapper._asset_with_portfolio(a, portfolio, load_snapshots=True)
                for a in model.assets
            ]
        return portfolio

    @staticmethod
    def asset_snapshot_to_domain(model: "AssetSnapshotModel") -> AssetSnapshot:
        return AssetSnapshot(
            id=UUID(model.id),
            asset_id=UUID(model.asset_id),
            value=model.value,
            observed_at=model.observed_at,
        )

    @staticmethod
    def portfolio_snapshot_to_domain(model: "PortfolioSnapshotModel") -> PortfolioSnapshot:
        return PortfolioSnapshot(
            id=UUID(model.id),
            portfolio_id=UUID(model.portfolio_id),
            value=model.value,
            observed_at=model.observed_at,
        )

    # ------------------------------------------------------------------
    # Domain → ORM (for save operations)
    # ------------------------------------------------------------------

    @staticmethod
    def tag_to_orm(entity: Tag) -> "TagModel":
        from app.adapters.outgoing.persistence.models.tag import TagModel
        return TagModel(id=str(entity.id), name=entity.name)

    @staticmethod
    def category_to_orm(entity: Category) -> "CategoryModel":
        from app.adapters.outgoing.persistence.models.category import CategoryModel
        return CategoryModel(
            id=str(entity.id),
            name=entity.name,
            parent_id=str(entity.parent.id) if entity.parent else None,
        )

    @staticmethod
    def portfolio_to_orm(entity: Portfolio) -> "PortfolioModel":
        from app.adapters.outgoing.persistence.models.portfolio import PortfolioModel
        return PortfolioModel(
            id=str(entity.id),
            name=entity.name,
            base_currency=entity.base_currency,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def asset_to_orm(entity: Asset) -> "AssetModel":
        from app.adapters.outgoing.persistence.models.asset import AssetModel
        return AssetModel(
            id=str(entity.id),
            portfolio_id=str(entity.portfolio.id),
            asset_type_id=str(entity.asset_type.id),
            name=entity.name,
            quantity=entity.quantity,
            disposed=entity.disposed,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            created_by=entity.created_by,
            updated_by=entity.updated_by,
        )

    @staticmethod
    def asset_snapshot_to_orm(entity: AssetSnapshot) -> "AssetSnapshotModel":
        from app.adapters.outgoing.persistence.models.asset_snapshot import AssetSnapshotModel
        return AssetSnapshotModel(
            id=str(entity.id),
            asset_id=str(entity.asset_id),
            value=entity.value,
            observed_at=entity.observed_at,
        )

    @staticmethod
    def portfolio_snapshot_to_orm(entity: PortfolioSnapshot) -> "PortfolioSnapshotModel":
        from app.adapters.outgoing.persistence.models.portfolio_snapshot import PortfolioSnapshotModel
        return PortfolioSnapshotModel(
            id=str(entity.id),
            portfolio_id=str(entity.portfolio_id),
            value=entity.value,
            observed_at=entity.observed_at,
        )
