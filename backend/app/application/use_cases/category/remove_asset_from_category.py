"""Use Case: Remove Asset from Category"""
from uuid import UUID
from pydantic import BaseModel
from app.domain.exceptions import AssetNotFound, CategoryNotFound
from app.domain.ports.repository import IAssetRepository, ICategoryRepository


class RemoveAssetFromCategoryCommand(BaseModel):
    asset_id: UUID
    category_id: UUID


class RemoveAssetFromCategoryUseCase:
    def __init__(self, asset_repository: IAssetRepository, category_repository: ICategoryRepository):
        self.asset_repository = asset_repository
        self.category_repository = category_repository

    def execute(self, command: RemoveAssetFromCategoryCommand) -> None:
        asset = self.asset_repository.find_by_id(str(command.asset_id))
        if not asset:
            raise AssetNotFound(f"Asset with id {command.asset_id} not found.")

        category = self.category_repository.find_by_id(str(command.category_id))
        if not category:
            raise CategoryNotFound(f"Category with id {command.category_id} not found.")

        self.asset_repository.remove_category(str(command.asset_id), str(command.category_id))
