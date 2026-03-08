"""Use Case: Update Portfolio"""
from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel
from app.domain.exceptions import PortfolioNotFound
from app.domain.ports.repository import IPortfolioRepository


class UpdatePortfolioCommand(BaseModel):
    portfolio_id: UUID
    name: str
    base_currency: str = "EUR"


class UpdatePortfolioUseCase:
    def __init__(self, portfolio_repository: IPortfolioRepository):
        self.portfolio_repository = portfolio_repository

    def execute(self, command: UpdatePortfolioCommand):
        portfolio = self.portfolio_repository.find_by_id(str(command.portfolio_id))
        if not portfolio:
            raise PortfolioNotFound(f"Portfolio with id {command.portfolio_id} not found.")
        
        portfolio.name = command.name
        portfolio.base_currency = command.base_currency
        portfolio.updated_at = datetime.now(timezone.utc)
        return self.portfolio_repository.save(portfolio)
