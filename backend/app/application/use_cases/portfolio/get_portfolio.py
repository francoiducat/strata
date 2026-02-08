"""
Use Case: Get Portfolio
"""
from uuid import UUID

from app.domain.entities.portfolio import Portfolio
from app.domain.exceptions import PortfolioNotFound
from app.domain.ports.repository import IPortfolioRepository


class GetPortfolioUseCase:
    """
    Use case for retrieving a single portfolios, including its assets.
    """
    def __init__(self, portfolio_repository: IPortfolioRepository):
        self.portfolio_repository = portfolio_repository

    def execute(self, portfolio_id: UUID) -> Portfolio:
        """
        Fetches a portfolios by its ID, eagerly loading its assets.

        Raises:
            PortfolioNotFound: If no portfolios with the given ID is found.
        """
        portfolio = self.portfolio_repository.find_with_assets(portfolio_id)
        if portfolio is None:
            raise PortfolioNotFound(f"Portfolio with id {portfolio_id} not found.")
        return portfolio
