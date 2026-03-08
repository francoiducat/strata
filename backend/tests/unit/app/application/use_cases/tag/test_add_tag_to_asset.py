"""Unit tests for AddTagToAssetUseCase."""
import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.use_cases.tag.add_tag_to_asset import AddTagToAssetUseCase, AddTagToAssetCommand
from app.domain.exceptions import AssetNotFound, TagNotFound


def make_fake_asset(id_=None):
    asset = MagicMock()
    asset.id = str(id_ or uuid4())
    return asset


def make_fake_tag(id_=None, name="test-tag"):
    tag = MagicMock()
    tag.id = str(id_ or uuid4())
    tag.name = name
    return tag


def test_add_tag_to_asset_success(dummy_asset_repository, dummy_tag_repository):
    asset_id = uuid4()
    tag_id = uuid4()

    asset = make_fake_asset(asset_id)
    dummy_asset_repository.save(asset)
    tag = make_fake_tag(tag_id)
    dummy_tag_repository.save(tag)

    use_case = AddTagToAssetUseCase(dummy_asset_repository, dummy_tag_repository)
    command = AddTagToAssetCommand(asset_id=asset_id, tag_id=tag_id)
    result = use_case.execute(command)

    assert result is not None


def test_add_tag_to_asset_asset_not_found(dummy_asset_repository, dummy_tag_repository):
    tag_id = uuid4()
    tag = make_fake_tag(tag_id)
    dummy_tag_repository.save(tag)

    use_case = AddTagToAssetUseCase(dummy_asset_repository, dummy_tag_repository)
    command = AddTagToAssetCommand(asset_id=uuid4(), tag_id=tag_id)
    with pytest.raises(AssetNotFound):
        use_case.execute(command)


def test_add_tag_to_asset_tag_not_found(dummy_asset_repository, dummy_tag_repository):
    asset_id = uuid4()
    asset = make_fake_asset(asset_id)
    dummy_asset_repository.save(asset)

    use_case = AddTagToAssetUseCase(dummy_asset_repository, dummy_tag_repository)
    command = AddTagToAssetCommand(asset_id=asset_id, tag_id=uuid4())
    with pytest.raises(TagNotFound):
        use_case.execute(command)
