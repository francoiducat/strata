"""Use Case: Delete Tag"""
from uuid import UUID
from app.domain.exceptions import TagNotFound
from app.domain.ports.repository import ITagRepository


class DeleteTagUseCase:
    def __init__(self, tag_repository: ITagRepository):
        self.tag_repository = tag_repository

    def execute(self, tag_id: UUID) -> None:
        tag = self.tag_repository.find_by_id(str(tag_id))
        if not tag:
            raise TagNotFound(f"Tag with id {tag_id} not found.")
        self.tag_repository.delete(str(tag_id))
