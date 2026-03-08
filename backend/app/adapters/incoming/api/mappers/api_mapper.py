"""
Maps domain entities to API response schemas.
"""
from typing import List, Optional
from uuid import UUID

from app.domain.entities.asset import Asset
from app.domain.entities.asset_snapshot import AssetSnapshot
from app.domain.entities.asset_type import AssetType
from app.domain.entities.category import Category
from app.domain.entities.portfolio import Portfolio
from app.domain.entities.portfolio_snapshot import PortfolioSnapshot
from app.domain.entities.tag import Tag
from ..schemas.asset_response import AssetResponse
from ..schemas.asset_snapshot_response import AssetSnapshotResponse
from ..schemas.asset_type_response import AssetTypeResponse
from ..schemas.category_response import CategoryResponse
from ..schemas.portfolio_response import PortfolioResponse
from ..schemas.portfolio_snapshot_response import PortfolioSnapshotResponse
from ..schemas.tag_response import TagResponse


class ApiMapper:
    """Translates domain entities to API response DTOs."""

    @staticmethod
    def to_asset_response(asset: Asset) -> AssetResponse:
        return AssetResponse.model_validate(asset)

    @staticmethod
    def to_asset_response_list(assets: List[Asset]) -> List[AssetResponse]:
        return [ApiMapper.to_asset_response(a) for a in assets]

    @staticmethod
    def to_portfolio_response(portfolio: Portfolio) -> PortfolioResponse:
        return PortfolioResponse(
            id=portfolio.id,
            name=portfolio.name,
            base_currency=portfolio.base_currency,
            total_value=portfolio.total_value(),
            created_at=portfolio.created_at,
            updated_at=portfolio.updated_at,
        )

    @staticmethod
    def to_portfolio_response_list(portfolios: List[Portfolio]) -> List[PortfolioResponse]:
        return [ApiMapper.to_portfolio_response(p) for p in portfolios]

    @staticmethod
    def to_portfolio_snapshot_response(snapshot: PortfolioSnapshot) -> PortfolioSnapshotResponse:
        return PortfolioSnapshotResponse.model_validate(snapshot)

    @staticmethod
    def to_portfolio_snapshot_response_list(snapshots: List[PortfolioSnapshot]) -> List[PortfolioSnapshotResponse]:
        return [ApiMapper.to_portfolio_snapshot_response(s) for s in snapshots]

    @staticmethod
    def to_asset_type_response(asset_type: AssetType) -> AssetTypeResponse:
        return AssetTypeResponse.model_validate(asset_type)

    @staticmethod
    def to_asset_type_response_list(asset_types: List[AssetType]) -> List[AssetTypeResponse]:
        return [ApiMapper.to_asset_type_response(at) for at in asset_types]

    @staticmethod
    def to_category_response(category: Category) -> CategoryResponse:
        parent_id: Optional[UUID] = category.parent.id if category.parent else None
        return CategoryResponse(id=category.id, name=category.name, parent_id=parent_id)

    @staticmethod
    def to_category_response_list(categories: List[Category]) -> List[CategoryResponse]:
        return [ApiMapper.to_category_response(c) for c in categories]

    @staticmethod
    def to_tag_response(tag: Tag) -> TagResponse:
        return TagResponse.model_validate(tag)

    @staticmethod
    def to_tag_response_list(tags: List[Tag]) -> List[TagResponse]:
        return [ApiMapper.to_tag_response(t) for t in tags]

    @staticmethod
    def to_asset_snapshot_response(snapshot: AssetSnapshot) -> AssetSnapshotResponse:
        return AssetSnapshotResponse.model_validate(snapshot)

    @staticmethod
    def to_asset_snapshot_response_list(snapshots: List[AssetSnapshot]) -> List[AssetSnapshotResponse]:
        return [ApiMapper.to_asset_snapshot_response(s) for s in snapshots]
