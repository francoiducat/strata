"""Unit tests for CreateCategoryUseCase."""
import pytest
from uuid import uuid4

from app.application.use_cases.category.create_category import CreateCategoryUseCase, CreateCategoryCommand
from app.domain.entities.category import Category
from app.domain.exceptions import DuplicateName, CategoryNotFound


def make_fake_category(id_=None, name="Parent", parent=None):
    return Category(id=id_ or uuid4(), name=name, parent=parent)


def test_create_category_no_parent(dummy_category_repository):
    use_case = CreateCategoryUseCase(dummy_category_repository)
    command = CreateCategoryCommand(name="Equities")
    result = use_case.execute(command)

    assert result.id is not None
    assert result.name == "Equities"
    assert result.parent is None


def test_create_category_with_parent(dummy_category_repository):
    parent_id = uuid4()
    parent = make_fake_category(parent_id, name="Parent")
    dummy_category_repository.save(parent)

    use_case = CreateCategoryUseCase(dummy_category_repository)
    command = CreateCategoryCommand(name="Child", parent_id=parent_id)
    result = use_case.execute(command)

    assert result.name == "Child"
    assert result.parent is not None
    assert str(result.parent.id) == str(parent_id)


def test_create_category_duplicate_name(dummy_category_repository):
    existing = make_fake_category(name="Equities")
    dummy_category_repository.save(existing)

    use_case = CreateCategoryUseCase(dummy_category_repository)
    command = CreateCategoryCommand(name="Equities")
    with pytest.raises(DuplicateName):
        use_case.execute(command)


def test_create_category_parent_not_found(dummy_category_repository):
    use_case = CreateCategoryUseCase(dummy_category_repository)
    command = CreateCategoryCommand(name="Child", parent_id=uuid4())
    with pytest.raises(CategoryNotFound):
        use_case.execute(command)
