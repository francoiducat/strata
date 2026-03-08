"""Use Case: Get Tag by ID"""
from uuid import UUID
from app.domain.exceptions import TagNotFound
from app.domain.ports.repository import ITagRepository


class GetTagUseCase:
    def __init__(self, tag_repository: ITagRepository):
        self.tag_repository = tag_repository

    def execute(self, tag_id: UUID):
        tag = self.tag_repository.find_by_id(str(tag_id))
        if not tag:
            raise TagNotFound(f"Tag with id {tag_id} not found.")
        return tag
