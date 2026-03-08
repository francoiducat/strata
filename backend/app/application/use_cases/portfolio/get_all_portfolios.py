"""Use Case: Get All Portfolios"""
from typing import List
from app.domain.entities.portfolio import Portfolio
from app.domain.ports.repository import IPortfolioRepository


class GetAllPortfoliosUseCase:
    """Use case for retrieving all portfolios."""

    def __init__(self, portfolio_repository: IPortfolioRepository):
        self.portfolio_repository = portfolio_repository

    def execute(self) -> List[Portfolio]:
        return self.portfolio_repository.find_all()
