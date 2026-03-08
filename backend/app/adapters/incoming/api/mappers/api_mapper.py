"""
Maps domain entities to API response schemas.
"""
from decimal import Decimal
from typing import List, Any

from app.domain.entities.asset import Asset
from app.domain.entities.portfolio import Portfolio
from ..schemas.asset_response import AssetResponse
from ..schemas.portfolio_response import PortfolioResponse
from ..schemas.portfolio_snapshot_response import PortfolioSnapshotResponse


class ApiMapper:
    """
    Translates between domain entities and API Data Transfer Objects (DTOs),
    which are Pydantic schemas.
    """

    @staticmethod
    def to_asset_response(asset: Asset) -> AssetResponse:
        return AssetResponse.model_validate(asset)

    @staticmethod
    def to_asset_response_list(assets: List[Asset]) -> List[AssetResponse]:
        return [ApiMapper.to_asset_response(asset) for asset in assets]

    @staticmethod
    def to_portfolio_response(portfolio: Any) -> PortfolioResponse:
        # Accept either domain Portfolio or SQLAlchemy PortfolioModel.
        # total_value is computed here from loaded ORM relationships because
        # routes pass PortfolioModel (ORM), not the domain entity.
        loaded_assets = getattr(portfolio, "assets", None) or []
        total_value = sum(
            (
                Decimal(str(asset.snapshots[0].value))
                for asset in loaded_assets
                if not asset.disposed and asset.snapshots
            ),
            Decimal("0"),
        )
        try:
            response = PortfolioResponse.model_validate(portfolio)
        except Exception:
            response = PortfolioResponse(
                id=getattr(portfolio, "id"),
                name=getattr(portfolio, "name"),
                base_currency=getattr(portfolio, "base_currency", "EUR"),
                created_at=getattr(portfolio, "created_at"),
                updated_at=getattr(portfolio, "updated_at"),
            )
        return response.model_copy(update={"total_value": total_value})

    @staticmethod
    def to_portfolio_response_list(portfolios: List[Portfolio]) -> List[PortfolioResponse]:
        return [ApiMapper.to_portfolio_response(portfolio) for portfolio in portfolios]

    @staticmethod
    def to_portfolio_snapshot_response(snapshot: Any) -> PortfolioSnapshotResponse:
        return PortfolioSnapshotResponse.model_validate(snapshot)

    @staticmethod
    def to_portfolio_snapshot_response_list(snapshots: List[Any]) -> List[PortfolioSnapshotResponse]:
        return [ApiMapper.to_portfolio_snapshot_response(s) for s in snapshots]
