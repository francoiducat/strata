"""Use Case: Create Category"""
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from app.domain.entities.category import Category
from app.domain.exceptions import CategoryNotFound
from app.domain.exceptions.Exceptions import DuplicateName
from app.domain.ports.repository import ICategoryRepository


class CreateCategoryCommand(BaseModel):
    name: str
    parent_id: Optional[UUID] = None


class CreateCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def execute(self, command: CreateCategoryCommand) -> Category:
        existing = self.category_repository.find_by_name(command.name)
        if existing:
            raise DuplicateName(f"Category with name '{command.name}' already exists.")

        parent: Optional[Category] = None
        if command.parent_id:
            parent = self.category_repository.find_by_id(str(command.parent_id))
            if not parent:
                raise CategoryNotFound(f"Parent category with id {command.parent_id} not found.")

        new_category = Category(id=uuid4(), name=command.name, parent=parent)
        return self.category_repository.save(new_category)
