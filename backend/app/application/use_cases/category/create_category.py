"""
Use Case: Create Category
"""
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

from app.domain.entities.category import Category
from app.domain.exceptions import CategoryNotFound
from app.domain.ports.repository import ICategoryRepository


class CreateCategoryCommand(BaseModel):
    """
    DTO for creating a new category.
    """
    name: str
    parent_id: Optional[UUID] = None


class CreateCategoryUseCase:
    """
    Use case for creating a new category.
    """
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def execute(self, command: CreateCategoryCommand) -> Category:
        """
        Creates and persists a new category.

        Raises:
            CategoryNotFound: If the parent category does not exist.
        """
        parent_category = None
        if command.parent_id:
            parent_category = self.category_repository.find_by_id(command.parent_id)
            if not parent_category:
                raise CategoryNotFound(f"Parent category with id {command.parent_id} not found.")

        new_category = Category(
            id=uuid4(), name=command.name, parent=parent_category
        )

        return self.category_repository.save(new_category)

