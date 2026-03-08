"""Unit tests for delete_asset and get_all_assets use cases."""
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.application.use_cases.asset.delete_asset import DeleteAssetUseCase
from app.application.use_cases.asset.get_all_assets import GetAllAssetsUseCase
from app.domain.entities.asset import Asset
from app.domain.entities.asset_type import AssetType
from app.domain.entities.portfolio import Portfolio
from app.domain.exceptions import AssetNotFound


def _now():
    return datetime.now(timezone.utc)


def make_asset():
    p = Portfolio(id=uuid4(), name="P", base_currency="EUR", created_at=_now(), updated_at=_now())
    return Asset(
        id=uuid4(), name="A",
        asset_type=AssetType(id=uuid4(), code="EQ", label="Equity"),
        portfolio=p,
        created_at=_now(), updated_at=_now(),
        created_by="u", updated_by="u",
    )


class TestDeleteAssetUseCase:
    def test_delete_success(self, dummy_asset_repository):
        asset = make_asset()
        dummy_asset_repository.save(asset)
        use_case = DeleteAssetUseCase(dummy_asset_repository)
        result = use_case.execute(asset.id)
        assert result is None

    def test_delete_not_found(self, dummy_asset_repository):
        use_case = DeleteAssetUseCase(dummy_asset_repository)
        with pytest.raises(AssetNotFound):
            use_case.execute(uuid4())


class TestGetAllAssetsUseCase:
    def test_empty(self, dummy_asset_repository):
        use_case = GetAllAssetsUseCase(dummy_asset_repository)
        assert use_case.execute() == []

    def test_with_items(self, dummy_asset_repository):
        asset = make_asset()
        dummy_asset_repository.save(asset)
        use_case = GetAllAssetsUseCase(dummy_asset_repository)
        result = use_case.execute()
        assert len(result) == 1
