"""
Use Case: Add Asset to Category
"""
from uuid import UUID

from pydantic import BaseModel

from app.adapters.outgoing.persistence.models.asset import AssetModel
from app.domain.exceptions import AssetNotFound, CategoryNotFound
from app.domain.ports.repository import IAssetRepository, ICategoryRepository


class AddAssetToCategoryCommand(BaseModel):
    """
    DTO for associating an asset with a category.
    """
    asset_id: UUID
    category_id: UUID


class AddAssetToCategoryUseCase:
    """
    Use case for adding an asset to a category.
    """

    def __init__(
        self,
        asset_repository: IAssetRepository,
        category_repository: ICategoryRepository,
    ):
        self.asset_repository = asset_repository
        self.category_repository = category_repository

    def execute(self, command: AddAssetToCategoryCommand) -> AssetModel:
        """
        Associates an asset with a category and persists the change.

        Raises:
            AssetNotFound: If the asset does not exist.
            CategoryNotFound: If the category does not exist.
        """
        asset = self.asset_repository.find_by_id(str(command.asset_id))
        if not asset:
            raise AssetNotFound(f"Asset with id {command.asset_id} not found.")

        category = self.category_repository.find_by_id(str(command.category_id))
        if not category:
            raise CategoryNotFound(f"Category with id {command.category_id} not found.")

        self.asset_repository.add_category(str(command.asset_id), str(command.category_id))
        return asset

