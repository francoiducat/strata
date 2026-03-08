"""Use Case: Create Tag"""
from uuid import uuid4
from pydantic import BaseModel
from app.domain.entities.tag import Tag
from app.domain.exceptions import DuplicateName
from app.domain.ports.repository import ITagRepository


class CreateTagCommand(BaseModel):
    name: str


class CreateTagUseCase:
    def __init__(self, tag_repository: ITagRepository):
        self.tag_repository = tag_repository

    def execute(self, command: CreateTagCommand) -> Tag:
        existing = self.tag_repository.find_by_name(command.name)
        if existing:
            raise DuplicateName(f"Tag with name '{command.name}' already exists.")
        new_tag = Tag(id=uuid4(), name=command.name)
        return self.tag_repository.save(new_tag)
