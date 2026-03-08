"""Unit tests for CreateAssetSnapshotUseCase."""
import pytest
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.use_cases.asset_snapshot.create_asset_snapshot import CreateAssetSnapshotUseCase
from app.domain.exceptions import AssetNotFound


def make_fake_asset(id_=None):
    asset = MagicMock()
    asset.id = str(id_ or uuid4())
    return asset


def test_create_snapshot_success(dummy_asset_repository, dummy_asset_snapshot_repository):
    asset_id = uuid4()
    asset = make_fake_asset(asset_id)
    dummy_asset_repository.save(asset)

    use_case = CreateAssetSnapshotUseCase(dummy_asset_snapshot_repository, dummy_asset_repository)
    result = use_case.execute(str(asset_id), Decimal("1234.56"))

    assert result.id is not None
    assert str(result.asset_id) == str(asset_id)
    assert result.value == Decimal("1234.56")


def test_create_snapshot_asset_not_found(dummy_asset_repository, dummy_asset_snapshot_repository):
    use_case = CreateAssetSnapshotUseCase(dummy_asset_snapshot_repository, dummy_asset_repository)
    with pytest.raises(AssetNotFound):
        use_case.execute(str(uuid4()), Decimal("100.00"))
