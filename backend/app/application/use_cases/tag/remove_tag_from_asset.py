"""Use Case: Remove Tag from Asset"""
from uuid import UUID
from pydantic import BaseModel
from app.domain.exceptions import AssetNotFound, TagNotFound
from app.domain.ports.repository import IAssetRepository, ITagRepository


class RemoveTagFromAssetCommand(BaseModel):
    asset_id: UUID
    tag_id: UUID


class RemoveTagFromAssetUseCase:
    def __init__(self, asset_repository: IAssetRepository, tag_repository: ITagRepository):
        self.asset_repository = asset_repository
        self.tag_repository = tag_repository

    def execute(self, command: RemoveTagFromAssetCommand) -> None:
        asset = self.asset_repository.find_by_id(str(command.asset_id))
        if not asset:
            raise AssetNotFound(f"Asset with id {command.asset_id} not found.")
        
        tag = self.tag_repository.find_by_id(str(command.tag_id))
        if not tag:
            raise TagNotFound(f"Tag with id {command.tag_id} not found.")
        
        self.asset_repository.remove_tag(str(command.asset_id), str(command.tag_id))
