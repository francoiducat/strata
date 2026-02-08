"""
Portfolio-related dependency providers: DB session, repository and portfolio use-cases.
Single-responsibility: this module only exposes portfolio-related DI providers.
"""
from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.portfolio.create_portfolio import CreatePortfolioUseCase
from app.application.use_cases.portfolio.get_portfolio import GetPortfolioUseCase
from app.application.use_cases.portfolio.delete_portfolio import DeletePortfolioUseCase
from app.application.use_cases.portfolio.get_all_portfolios import GetAllPortfoliosUseCase
from app.domain.ports.repository import IPortfolioRepository
from app.adapters.outgoing.persistence.database import SessionLocal
from app.adapters.outgoing.persistence.repository.sqlalchemy_portfolio_repository import SQLAlchemyPortfolioRepository


# Dependency to get a DB session
def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Repository provider for portfolios
def get_portfolio_repository(db: Session = Depends(get_db_session)) -> IPortfolioRepository:
    return SQLAlchemyPortfolioRepository(db)


# Portfolio use case providers
def create_portfolio_use_case(
    portfolio_repository: IPortfolioRepository = Depends(get_portfolio_repository),
) -> CreatePortfolioUseCase:
    return CreatePortfolioUseCase(portfolio_repository)


def get_portfolio_use_case(
    portfolio_repository: IPortfolioRepository = Depends(get_portfolio_repository),
) -> GetPortfolioUseCase:
    return GetPortfolioUseCase(portfolio_repository)


def delete_portfolio_use_case(
    portfolio_repository: IPortfolioRepository = Depends(get_portfolio_repository),
) -> DeletePortfolioUseCase:
    return DeletePortfolioUseCase(portfolio_repository)


def get_all_portfolios_use_case(
    portfolio_repository: IPortfolioRepository = Depends(get_portfolio_repository),
) -> GetAllPortfoliosUseCase:
    return GetAllPortfoliosUseCase(portfolio_repository)


__all__ = [
    'get_db_session',
    'get_portfolio_repository',
    'create_portfolio_use_case',
    'get_portfolio_use_case',
    'delete_portfolio_use_case',
    'get_all_portfolios_use_case',
]
