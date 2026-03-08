"""Unit tests for GetAllCategoriesUseCase."""
from uuid import uuid4

from app.application.use_cases.category.get_all_categories import GetAllCategoriesUseCase
from app.domain.entities.category import Category


def test_get_all_categories_empty(dummy_category_repository):
    use_case = GetAllCategoriesUseCase(dummy_category_repository)
    assert use_case.execute() == []


def test_get_all_categories_with_items(dummy_category_repository):
    c1 = Category(id=uuid4(), name="Bonds")
    c2 = Category(id=uuid4(), name="Stocks")
    dummy_category_repository.save(c1)
    dummy_category_repository.save(c2)
    use_case = GetAllCategoriesUseCase(dummy_category_repository)
    result = use_case.execute()
    assert len(result) == 2
