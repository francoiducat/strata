"""
Transaction Domain Entity
"""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from pydantic.config import ConfigDict


class Transaction(BaseModel):
    """
    Transaction domain entity. Records acquisitions, disposals, and adjustments.
    """
    id: UUID
    type: str
    quantity: Decimal
    unit_price: Decimal
    currency: str
    occurred_at: datetime

    model_config = ConfigDict(from_attributes=True)
