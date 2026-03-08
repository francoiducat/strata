"""Unit tests for GetTagUseCase."""
import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.use_cases.tag.get_tag import GetTagUseCase
from app.domain.exceptions import TagNotFound


def make_fake_tag(id_=None, name="test-tag"):
    tag = MagicMock()
    tag.id = str(id_ or uuid4())
    tag.name = name
    return tag


def test_get_tag_found(dummy_tag_repository):
    tag_id = uuid4()
    tag = make_fake_tag(tag_id, name="growth")
    dummy_tag_repository.save(tag)

    use_case = GetTagUseCase(dummy_tag_repository)
    result = use_case.execute(tag_id)

    assert str(result.id) == str(tag_id)
    assert result.name == "growth"


def test_get_tag_not_found(dummy_tag_repository):
    use_case = GetTagUseCase(dummy_tag_repository)
    with pytest.raises(TagNotFound):
        use_case.execute(uuid4())
