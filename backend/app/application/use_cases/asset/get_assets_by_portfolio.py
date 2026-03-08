"""Use Case: Get Assets by Portfolio"""
from typing import List
from uuid import UUID
from app.domain.exceptions import PortfolioNotFound
from app.domain.ports.repository import IAssetRepository, IPortfolioRepository


class GetAssetsByPortfolioUseCase:
    def __init__(self, asset_repository: IAssetRepository, portfolio_repository: IPortfolioRepository):
        self.asset_repository = asset_repository
        self.portfolio_repository = portfolio_repository

    def execute(self, portfolio_id: UUID) -> List:
        portfolio = self.portfolio_repository.find_by_id(str(portfolio_id))
        if not portfolio:
            raise PortfolioNotFound(f"Portfolio with id {portfolio_id} not found.")
        return self.asset_repository.find_by_portfolio(str(portfolio_id))
