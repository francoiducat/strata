"""
Use Case: Delete Portfolio
"""
from uuid import UUID

from app.domain.exceptions import PortfolioNotFound
from app.domain.ports.repository import IPortfolioRepository


class DeletePortfolioUseCase:
    """
    Use case for deleting a portfolios.
    """

    def __init__(self, portfolio_repository: IPortfolioRepository):
        self.portfolio_repository = portfolio_repository

    def execute(self, portfolio_id: UUID) -> None:
        """
        Delete a portfolios by id. Raises PortfolioNotFound if it does not exist.
        """
        deleted = self.portfolio_repository.delete(str(portfolio_id))
        if not deleted:
            raise PortfolioNotFound(f"Portfolio with id {portfolio_id} not found.")
        return None
