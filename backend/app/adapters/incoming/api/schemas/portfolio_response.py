from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic.config import ConfigDict


class PortfolioResponse(BaseModel):
    id: UUID
    name: str
    base_currency: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
