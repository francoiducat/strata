"""
Use Case: Update Asset
"""
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.domain.entities.asset import Asset
from app.domain.exceptions import AssetNotFound
from app.domain.ports.repository import IAssetRepository


class UpdateAssetCommand(BaseModel):
    """
    DTO for updating an asset.
    """
    asset_id: UUID
    name: str
    quantity: Optional[Decimal] = None
    updated_by: str


class UpdateAssetUseCase:
    """
    Use case for updating an existing asset's details.
    """
    def __init__(self, asset_repository: IAssetRepository):
        self.asset_repository = asset_repository

    def execute(self, command: UpdateAssetCommand) -> Asset:
        """
        Updates, validates, and persists an asset.

        Raises:
            AssetNotFound: If the asset does not exist.
        """
        asset = self.asset_repository.find_by_id(command.asset_id)
        if not asset:
            raise AssetNotFound(f"Asset with id {command.asset_id} not found.")

        # Update fields
        asset.name = command.name
        asset.quantity = command.quantity
        asset.updated_by = command.updated_by
        asset.updated_at = datetime.now(timezone.utc)

        return self.asset_repository.save(asset)
