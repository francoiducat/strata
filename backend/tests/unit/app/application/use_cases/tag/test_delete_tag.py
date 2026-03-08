"""Unit tests for DeleteTagUseCase."""
import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.use_cases.tag.delete_tag import DeleteTagUseCase
from app.domain.exceptions import TagNotFound


def make_fake_tag(id_=None, name="test-tag"):
    tag = MagicMock()
    tag.id = str(id_ or uuid4())
    tag.name = name
    return tag


def test_delete_tag_success(dummy_tag_repository):
    tag_id = uuid4()
    tag = make_fake_tag(tag_id, name="growth")
    dummy_tag_repository.save(tag)

    use_case = DeleteTagUseCase(dummy_tag_repository)
    use_case.execute(tag_id)

    assert dummy_tag_repository.find_by_id(str(tag_id)) is None


def test_delete_tag_not_found(dummy_tag_repository):
    use_case = DeleteTagUseCase(dummy_tag_repository)
    with pytest.raises(TagNotFound):
        use_case.execute(uuid4())
