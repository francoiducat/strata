"""
Use Case: Get All Portfolios
"""
from typing import List, Any

from app.domain.ports.repository import IPortfolioRepository


class GetAllPortfoliosUseCase:
    """Use case for retrieving all portfolios."""

    def __init__(self, portfolio_repository: IPortfolioRepository):
        self.portfolio_repository = portfolio_repository

    def execute(self) -> List[Any]:
        """Return list of portfolios (repository may return domain objects or ORM models)."""
        return self.portfolio_repository.find_all()
