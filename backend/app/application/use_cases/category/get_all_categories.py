"""Use Case: Get All Categories"""
from typing import List
from app.domain.ports.repository import ICategoryRepository


class GetAllCategoriesUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def execute(self) -> List:
        return self.category_repository.find_all()
