"""
Use Case: Create Portfolio
"""
from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel

from app.domain.entities.portfolio import Portfolio
from app.domain.ports.repository import IPortfolioRepository
from app.adapters.outgoing.persistence.models import PortfolioModel


class CreatePortfolioCommand(BaseModel):
    """
    DTO for creating a new portfolios.
    """
    name: str
    base_currency: str = "EUR"


class CreatePortfolioUseCase:
    """
    Use case for creating a new portfolios.
    """
    def __init__(self, portfolio_repository: IPortfolioRepository):
        self.portfolio_repository = portfolio_repository

    def execute(self, command: CreatePortfolioCommand) -> PortfolioModel:
        """
        Creates and persists a new portfolios as a SQLAlchemy model.
        """
        now = datetime.now(timezone.utc)
        new_portfolio = PortfolioModel(
            name=command.name,
            base_currency=command.base_currency,
            created_at=now,
            updated_at=now,
        )
        return self.portfolio_repository.save(new_portfolio)
