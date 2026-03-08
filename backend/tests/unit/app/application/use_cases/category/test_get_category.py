"""Unit tests for GetCategoryUseCase."""
import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.use_cases.category.get_category import GetCategoryUseCase
from app.domain.exceptions import CategoryNotFound


def make_fake_category(id_=None, name="Test"):
    cat = MagicMock()
    cat.id = str(id_ or uuid4())
    cat.name = name
    cat.parent_id = None
    return cat


def test_get_category_found(dummy_category_repository):
    cat_id = uuid4()
    cat = make_fake_category(cat_id, name="Equities")
    dummy_category_repository.save(cat)

    use_case = GetCategoryUseCase(dummy_category_repository)
    result = use_case.execute(cat_id)

    assert str(result.id) == str(cat_id)
    assert result.name == "Equities"


def test_get_category_not_found(dummy_category_repository):
    use_case = GetCategoryUseCase(dummy_category_repository)
    with pytest.raises(CategoryNotFound):
        use_case.execute(uuid4())
