"""Use Case: Delete Category"""
from uuid import UUID
from app.domain.exceptions import CategoryNotFound, CategoryHasChildren
from app.domain.ports.repository import ICategoryRepository


class DeleteCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def execute(self, category_id: UUID) -> None:
        category = self.category_repository.find_by_id(str(category_id))
        if not category:
            raise CategoryNotFound(f"Category with id {category_id} not found.")
        
        children = self.category_repository.find_children(str(category_id))
        if children:
            raise CategoryHasChildren(
                f"Cannot delete category '{category.name}' because it has {len(children)} child category(ies). "
                "Delete or reassign children first."
            )
        
        self.category_repository.delete(str(category_id))
