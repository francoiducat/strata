"""Unit tests for CreateTagUseCase."""
import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.use_cases.tag.create_tag import CreateTagUseCase, CreateTagCommand
from app.domain.exceptions import DuplicateName


def make_fake_tag(id_=None, name="test-tag"):
    tag = MagicMock()
    tag.id = str(id_ or uuid4())
    tag.name = name
    return tag


def test_create_tag_success(dummy_tag_repository):
    use_case = CreateTagUseCase(dummy_tag_repository)
    command = CreateTagCommand(name="growth")
    result = use_case.execute(command)

    assert result.id is not None
    assert result.name == "growth"


def test_create_tag_duplicate_name(dummy_tag_repository):
    existing = make_fake_tag(name="growth")
    dummy_tag_repository.save(existing)

    use_case = CreateTagUseCase(dummy_tag_repository)
    command = CreateTagCommand(name="growth")
    with pytest.raises(DuplicateName):
        use_case.execute(command)
