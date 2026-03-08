"""
Use Case: Create Category
"""
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

from app.adapters.outgoing.persistence.models.category import CategoryModel
from app.domain.exceptions import CategoryNotFound
from app.domain.exceptions.Exceptions import DuplicateName
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

    def execute(self, command: CreateCategoryCommand) -> CategoryModel:
        """
        Creates and persists a new category.

        Raises:
            DuplicateName: If a category with the same name already exists.
            CategoryNotFound: If the parent category does not exist.
        """
        existing = self.category_repository.find_by_name(command.name)
        if existing:
            raise DuplicateName(f"Category with name '{command.name}' already exists.")

        if command.parent_id:
            parent = self.category_repository.find_by_id(str(command.parent_id))
            if not parent:
                raise CategoryNotFound(f"Parent category with id {command.parent_id} not found.")

        new_category = CategoryModel(
            id=str(uuid4()),
            name=command.name,
            parent_id=str(command.parent_id) if command.parent_id else None,
        )

        return self.category_repository.save(new_category)

