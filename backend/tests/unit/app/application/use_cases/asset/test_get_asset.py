"""Unit tests for GetAssetUseCase (not-found path)."""
from uuid import uuid4

import pytest

from app.application.use_cases.asset.get_asset import GetAssetUseCase
from app.domain.exceptions import AssetNotFound


def test_get_asset_not_found(dummy_asset_repository):
    use_case = GetAssetUseCase(dummy_asset_repository)
    with pytest.raises(AssetNotFound):
        use_case.execute(uuid4())
