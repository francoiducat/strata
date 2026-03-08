"""Unit tests for AddAssetToCategoryUseCase."""
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.application.use_cases.category.add_asset_to_category import (
    AddAssetToCategoryUseCase,
    AddAssetToCategoryCommand,
)
from app.domain.entities.asset import Asset
from app.domain.entities.asset_type import AssetType
from app.domain.entities.category import Category
from app.domain.entities.portfolio import Portfolio
from app.domain.exceptions import AssetNotFound, CategoryNotFound


def make_asset(portfolio=None):
    now = datetime.now(timezone.utc)
    p = portfolio or Portfolio(id=uuid4(), name="P", base_currency="EUR", created_at=now, updated_at=now)
    return Asset(
        id=uuid4(), name="Asset",
        asset_type=AssetType(id=uuid4(), code="EQ", label="Equity"),
        portfolio=p,
        created_at=now, updated_at=now,
        created_by="u", updated_by="u",
    )


def make_category():
    return Category(id=uuid4(), name="Stocks")


def test_add_asset_to_category_success(dummy_asset_repository, dummy_category_repository):
    asset = make_asset()
    dummy_asset_repository.save(asset)
    category = make_category()
    dummy_category_repository.save(category)

    use_case = AddAssetToCategoryUseCase(dummy_asset_repository, dummy_category_repository)
    cmd = AddAssetToCategoryCommand(asset_id=asset.id, category_id=category.id)
    result = use_case.execute(cmd)
    assert result.id == asset.id


def test_add_asset_to_category_asset_not_found(dummy_asset_repository, dummy_category_repository):
    use_case = AddAssetToCategoryUseCase(dummy_asset_repository, dummy_category_repository)
    cmd = AddAssetToCategoryCommand(asset_id=uuid4(), category_id=uuid4())
    with pytest.raises(AssetNotFound):
        use_case.execute(cmd)


def test_add_asset_to_category_category_not_found(dummy_asset_repository, dummy_category_repository):
    asset = make_asset()
    dummy_asset_repository.save(asset)

    use_case = AddAssetToCategoryUseCase(dummy_asset_repository, dummy_category_repository)
    cmd = AddAssetToCategoryCommand(asset_id=asset.id, category_id=uuid4())
    with pytest.raises(CategoryNotFound):
        use_case.execute(cmd)
