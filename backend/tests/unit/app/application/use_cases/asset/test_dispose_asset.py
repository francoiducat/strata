"""Unit tests for DisposeAssetUseCase."""
import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.use_cases.asset.dispose_asset import DisposeAssetUseCase
from app.domain.exceptions import AssetNotFound


def make_fake_asset(id_=None, disposed=False):
    asset = MagicMock()
    asset.id = str(id_ or uuid4())
    asset.disposed = disposed
    return asset


def test_dispose_asset_success(dummy_asset_repository):
    asset_id = uuid4()
    asset = make_fake_asset(asset_id, disposed=False)
    dummy_asset_repository.save(asset)

    use_case = DisposeAssetUseCase(dummy_asset_repository)
    result = use_case.execute(asset_id)

    assert result.disposed is True


def test_dispose_asset_idempotent(dummy_asset_repository):
    asset_id = uuid4()
    asset = make_fake_asset(asset_id, disposed=True)
    dummy_asset_repository.save(asset)

    use_case = DisposeAssetUseCase(dummy_asset_repository)
    result = use_case.execute(asset_id)

    assert result.disposed is True


def test_dispose_asset_not_found(dummy_asset_repository):
    use_case = DisposeAssetUseCase(dummy_asset_repository)
    with pytest.raises(AssetNotFound):
        use_case.execute(uuid4())
