"""Use Case: Get Category by ID"""
from uuid import UUID
from app.domain.exceptions import CategoryNotFound
from app.domain.ports.repository import ICategoryRepository


class GetCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def execute(self, category_id: UUID):
        category = self.category_repository.find_by_id(str(category_id))
        if not category:
            raise CategoryNotFound(f"Category with id {category_id} not found.")
        return category
