"""
SQLAlchemy Transaction Repository Implementation

Concrete implementation of TransactionRepository using SQLAlchemy.
"""
from typing import Optional, cast
from datetime import datetime
from sqlalchemy.orm import Session

from app.domain.ports.repository.transaction_repository import ITransactionRepository
from app.adapters.outgoing.persistence.models import TransactionModel


class SQLAlchemyTransactionRepository(ITransactionRepository):
    """
    SQLAlchemy implementation of TransactionRepository.
    """

    def __init__(self, session: Session):
        """Initialize repository with persistence session."""
        self._session = session

    def save(self, entity: TransactionModel) -> TransactionModel:
        """Persist a transaction and return the saved entity."""
        self._session.add(entity)
        self._session.flush()
        return entity

    def find_by_id(self, entity_id: str) -> Optional[TransactionModel]:
        """Find transaction by id."""
        return self._session.query(TransactionModel).filter(TransactionModel.id == entity_id).first()

    def find_all(self) -> list[TransactionModel]:
        """Return all transactions."""
        return cast(list[TransactionModel], self._session.query(TransactionModel).all())

    def delete(self, entity_id: str) -> bool:
        """Delete transaction by id."""
        obj = self.find_by_id(entity_id)
        if obj:
            self._session.delete(obj)
            self._session.flush()
            return True
        return False

    def exists(self, entity_id: str) -> bool:
        """Check existence by id."""
        return self._session.query(
            self._session.query(TransactionModel).filter(TransactionModel.id == entity_id).exists()
        ).scalar()

    # Domain / interface-specific methods (keep in same order as the port)
    def find_by_asset(self, asset_id: str) -> list[TransactionModel]:
        """Find transactions related to an asset."""
        return cast(list[TransactionModel], self._session.query(TransactionModel).filter(TransactionModel.asset_id == asset_id).all())

    def find_between_dates(self, start_date: datetime, end_date: datetime) -> list[TransactionModel]:
        """Find transactions in a date range (using occurred_at field)."""
        q = self._session.query(TransactionModel)
        q = q.filter(TransactionModel.occurred_at >= start_date)
        q = q.filter(TransactionModel.occurred_at <= end_date)
        return cast(list[TransactionModel], q.all())
