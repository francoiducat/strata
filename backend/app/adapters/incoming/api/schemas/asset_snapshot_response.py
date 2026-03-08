"""Pydantic schema for AssetSnapshot API response."""
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel
from pydantic.config import ConfigDict


class AssetSnapshotResponse(BaseModel):
    id: UUID
    asset_id: UUID
    value: Decimal
    observed_at: datetime

    model_config = ConfigDict(from_attributes=True)
