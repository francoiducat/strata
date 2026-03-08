"""Unit tests for GetAllAssetTypesUseCase and GetAssetTypeUseCase."""
from uuid import uuid4

import pytest

from app.application.use_cases.asset_type.get_all_asset_types import GetAllAssetTypesUseCase
from app.application.use_cases.asset_type.get_asset_type import GetAssetTypeUseCase
from app.domain.entities.asset_type import AssetType
from app.domain.exceptions import AssetTypeNotFound


class FakeAssetTypeRepo:
    def __init__(self, items=None):
        self.storage = {str(i.id): i for i in (items or [])}

    def find_all(self):
        return list(self.storage.values())

    def find_by_id(self, id_):
        return self.storage.get(str(id_))


def test_get_all_asset_types_empty():
    use_case = GetAllAssetTypesUseCase(FakeAssetTypeRepo())
    assert use_case.execute() == []


def test_get_all_asset_types_with_items():
    at1 = AssetType(id=uuid4(), code="EQ", label="Equity")
    at2 = AssetType(id=uuid4(), code="CASH", label="Cash")
    use_case = GetAllAssetTypesUseCase(FakeAssetTypeRepo([at1, at2]))
    result = use_case.execute()
    assert len(result) == 2


def test_get_asset_type_success():
    at = AssetType(id=uuid4(), code="EQ", label="Equity")
    use_case = GetAssetTypeUseCase(FakeAssetTypeRepo([at]))
    result = use_case.execute(at.id)
    assert result.code == "EQ"


def test_get_asset_type_not_found():
    use_case = GetAssetTypeUseCase(FakeAssetTypeRepo())
    with pytest.raises(AssetTypeNotFound):
        use_case.execute(uuid4())
