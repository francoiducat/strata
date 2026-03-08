"""Unit tests for GetAssetSnapshotsUseCase."""
import pytest
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.use_cases.asset_snapshot.create_asset_snapshot import CreateAssetSnapshotUseCase
from app.application.use_cases.asset_snapshot.get_asset_snapshots import GetAssetSnapshotsUseCase
from app.domain.exceptions import AssetNotFound


def make_fake_asset(id_=None):
    asset = MagicMock()
    asset.id = str(id_ or uuid4())
    return asset


def test_get_snapshots_returns_list(dummy_asset_repository, dummy_asset_snapshot_repository):
    asset_id = uuid4()
    asset = make_fake_asset(asset_id)
    dummy_asset_repository.save(asset)

    # Create a snapshot first
    create_uc = CreateAssetSnapshotUseCase(dummy_asset_snapshot_repository, dummy_asset_repository)
    create_uc.execute(str(asset_id), Decimal("500.00"))

    use_case = GetAssetSnapshotsUseCase(dummy_asset_snapshot_repository, dummy_asset_repository)
    results = use_case.execute(asset_id)

    assert isinstance(results, list)
    assert len(results) == 1


def test_get_snapshots_asset_not_found(dummy_asset_repository, dummy_asset_snapshot_repository):
    use_case = GetAssetSnapshotsUseCase(dummy_asset_snapshot_repository, dummy_asset_repository)
    with pytest.raises(AssetNotFound):
        use_case.execute(uuid4())
