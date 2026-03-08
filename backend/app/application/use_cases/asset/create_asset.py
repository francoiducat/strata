"""
Use Case: Create Asset
"""
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

from app.adapters.outgoing.persistence.models.asset import AssetModel
from app.domain.exceptions.Exceptions import PortfolioNotFound, AssetTypeNotFound
from app.domain.ports.repository import IAssetRepository, IPortfolioRepository, IAssetTypeRepository


class CreateAssetRequest(BaseModel):
    """
    DTO for creating a new asset.
    """
    portfolio_id: UUID
    asset_type_id: UUID
    name: str
    quantity: Optional[Decimal] = None
    created_by: str


class CreateAssetUseCase:
    """
    Use case for creating a new asset.
    """
    def __init__(
        self,
        asset_repository: IAssetRepository,
        portfolio_repository: IPortfolioRepository,
        asset_type_repository: IAssetTypeRepository,
    ):
        self.asset_repository = asset_repository
        self.portfolio_repository = portfolio_repository
        self.asset_type_repository = asset_type_repository

    def execute(self, command: CreateAssetRequest) -> AssetModel:
        """
        Creates, validates, and persists a new asset.

        Args:
            command: The data needed to create the asset.

        Returns:
            The newly created AssetModel ORM instance.

        Raises:
            PortfolioNotFound: If the portfolios does not exist.
            AssetTypeNotFound: If the asset type does not exist.
        """
        portfolio = self.portfolio_repository.find_by_id(command.portfolio_id)
        if not portfolio:
            raise PortfolioNotFound(f"Portfolio with id {command.portfolio_id} not found.")

        asset_type = self.asset_type_repository.find_by_id(command.asset_type_id)
        if not asset_type:
            raise AssetTypeNotFound(f"AssetType with id {command.asset_type_id} not found.")

        now = datetime.now(timezone.utc)
        new_asset = AssetModel(
            id=str(uuid4()),
            portfolio_id=str(command.portfolio_id),
            asset_type_id=str(command.asset_type_id),
            name=command.name,
            quantity=command.quantity,
            disposed=False,
            created_at=now,
            updated_at=now,
            created_by=command.created_by,
            updated_by=command.created_by,
        )

        return self.asset_repository.save(new_asset)
