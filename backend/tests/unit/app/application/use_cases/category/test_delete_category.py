"""Unit tests for DeleteCategoryUseCase."""
import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.use_cases.category.delete_category import DeleteCategoryUseCase
from app.domain.exceptions import CategoryNotFound, CategoryHasChildren


def make_fake_category(id_=None, name="Test", parent_id=None):
    cat = MagicMock()
    cat.id = str(id_ or uuid4())
    cat.name = name
    cat.parent_id = str(parent_id) if parent_id else None
    return cat


def test_delete_category_success(dummy_category_repository):
    cat_id = uuid4()
    cat = make_fake_category(cat_id, name="Leaf")
    dummy_category_repository.save(cat)

    use_case = DeleteCategoryUseCase(dummy_category_repository)
    use_case.execute(cat_id)

    assert dummy_category_repository.find_by_id(str(cat_id)) is None


def test_delete_category_not_found(dummy_category_repository):
    use_case = DeleteCategoryUseCase(dummy_category_repository)
    with pytest.raises(CategoryNotFound):
        use_case.execute(uuid4())


def test_delete_category_has_children(dummy_category_repository):
    parent_id = uuid4()
    parent = make_fake_category(parent_id, name="Parent")
    dummy_category_repository.save(parent)

    child = make_fake_category(name="Child", parent_id=parent_id)
    dummy_category_repository.save(child)

    use_case = DeleteCategoryUseCase(dummy_category_repository)
    with pytest.raises(CategoryHasChildren):
        use_case.execute(parent_id)
