"""Unit tests for GetAllTagsUseCase."""
from uuid import uuid4

from app.application.use_cases.tag.get_all_tags import GetAllTagsUseCase
from app.domain.entities.tag import Tag


def test_get_all_tags_empty(dummy_tag_repository):
    use_case = GetAllTagsUseCase(dummy_tag_repository)
    assert use_case.execute() == []


def test_get_all_tags_with_items(dummy_tag_repository):
    t1 = Tag(id=uuid4(), name="crypto")
    t2 = Tag(id=uuid4(), name="growth")
    dummy_tag_repository.save(t1)
    dummy_tag_repository.save(t2)
    use_case = GetAllTagsUseCase(dummy_tag_repository)
    result = use_case.execute()
    assert len(result) == 2
