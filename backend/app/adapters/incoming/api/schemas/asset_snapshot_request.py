"""Pydantic schemas for AssetSnapshot API requests."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class AssetSnapshotCreateRequest(BaseModel):
    value: Decimal
    observed_at: Optional[datetime] = None
