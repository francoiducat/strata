"""Unit tests for UpdateAssetUseCase (not-found path)."""
from uuid import uuid4

import pytest

from app.application.use_cases.asset.update_asset import UpdateAssetUseCase, UpdateAssetCommand
from app.domain.exceptions import AssetNotFound


def test_update_asset_not_found(dummy_asset_repository):
    use_case = UpdateAssetUseCase(dummy_asset_repository)
    cmd = UpdateAssetCommand(asset_id=uuid4(), name="New", updated_by="user")
    with pytest.raises(AssetNotFound):
        use_case.execute(cmd)
