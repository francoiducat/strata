"""Use Case: Create Portfolio"""
from datetime import datetime, timezone
from uuid import uuid4
from pydantic import BaseModel
from app.domain.entities.portfolio import Portfolio
from app.domain.ports.repository import IPortfolioRepository


class CreatePortfolioCommand(BaseModel):
    name: str
    base_currency: str = "EUR"


class CreatePortfolioUseCase:
    def __init__(self, portfolio_repository: IPortfolioRepository):
        self.portfolio_repository = portfolio_repository

    def execute(self, command: CreatePortfolioCommand) -> Portfolio:
        now = datetime.now(timezone.utc)
        new_portfolio = Portfolio(
            id=uuid4(),
            name=command.name,
            base_currency=command.base_currency,
            created_at=now,
            updated_at=now,
        )
        return self.portfolio_repository.save(new_portfolio)
