"""
Maps domain entities to API response schemas.
"""
from typing import List, Any

from app.domain.entities.asset import Asset
from app.domain.entities.portfolio import Portfolio
from ..schemas.asset_response import AssetResponse
from ..schemas.portfolio_response import PortfolioResponse


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
        # Accept either domain Portfolio or SQLAlchemy PortfolioModel
        try:
            return PortfolioResponse.model_validate(portfolio)
        except Exception:
            # Fallback: create a dict from attributes
            data = {
                'id': getattr(portfolio, 'id', None),
                'name': getattr(portfolio, 'name', None),
                'base_currency': getattr(portfolio, 'base_currency', 'EUR'),
                'created_at': getattr(portfolio, 'created_at', None),
                'updated_at': getattr(portfolio, 'updated_at', None),
            }
            return PortfolioResponse.model_validate(data)

    @staticmethod
    def to_portfolio_response_list(portfolios: List[Portfolio]) -> List[PortfolioResponse]:
        return [ApiMapper.to_portfolio_response(portfolio) for portfolio in portfolios]
