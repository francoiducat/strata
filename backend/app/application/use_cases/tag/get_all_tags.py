"""Use Case: Get All Tags"""
from typing import List
from app.domain.ports.repository import ITagRepository


class GetAllTagsUseCase:
    def __init__(self, tag_repository: ITagRepository):
        self.tag_repository = tag_repository

    def execute(self) -> List:
        return self.tag_repository.find_all()
