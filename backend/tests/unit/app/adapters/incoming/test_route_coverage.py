"""Unit tests for uncovered route paths using mocked use cases."""
from decimal import Decimal
from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def _now():
    return datetime.now(timezone.utc)


def make_mock_asset():
    from datetime import datetime, timezone
    from app.domain.entities.asset import Asset
    from app.domain.entities.asset_type import AssetType
    from app.domain.entities.portfolio import Portfolio
    now = datetime.now(timezone.utc)
    p = Portfolio(id=uuid4(), name="P", base_currency="EUR", created_at=now, updated_at=now)
    at = AssetType(id=uuid4(), code="EQ", label="Equity")
    return Asset(
        id=uuid4(), name="Asset", asset_type=at, portfolio=p,
        created_at=now, updated_at=now, created_by="u", updated_by="u"
    )


def make_mock_snapshot():
    s = MagicMock()
    s.id = uuid4()
    s.asset_id = uuid4()
    s.value = Decimal("100.0")
    s.observed_at = _now()
    return s


def make_mock_portfolio():
    p = MagicMock()
    p.id = uuid4()
    p.name = "P"
    p.base_currency = "EUR"
    p.created_at = _now()
    p.updated_at = _now()
    p.total_value = MagicMock(return_value=Decimal("0"))
    return p


def make_mock_portfolio_snapshot():
    s = MagicMock()
    s.id = uuid4()
    s.portfolio_id = uuid4()
    s.value = Decimal("500.0")
    s.observed_at = _now()
    return s


def make_mock_tag():
    t = MagicMock()
    t.id = uuid4()
    t.name = "mytag"
    return t


def make_mock_asset_type():
    at = MagicMock()
    at.id = uuid4()
    at.code = "EQ"
    at.label = "Equity"
    return at


class TestAssetRouteCoverage:
    def test_get_all_assets_with_portfolio_filter(self):
        from app.adapters.incoming.api.dependencies.assets import get_assets_by_portfolio_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = []
        app.dependency_overrides[get_assets_by_portfolio_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.get(f"/api/v1/assets/?portfolio_id={uuid4()}")
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.pop(get_assets_by_portfolio_use_case, None)

    def test_delete_asset_success(self):
        from app.adapters.incoming.api.dependencies.assets import delete_asset_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = None
        app.dependency_overrides[delete_asset_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.delete(f"/api/v1/assets/{uuid4()}")
            assert resp.status_code == 204
        finally:
            app.dependency_overrides.pop(delete_asset_use_case, None)

    def test_get_asset_snapshots_success(self):
        from app.adapters.incoming.api.dependencies.asset_snapshots import get_asset_snapshots_use_case
        mock_uc = MagicMock()
        snap = make_mock_snapshot()
        mock_uc.execute.return_value = [snap]
        app.dependency_overrides[get_asset_snapshots_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.get(f"/api/v1/assets/{uuid4()}/snapshots")
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.pop(get_asset_snapshots_use_case, None)

    def test_add_tag_to_asset_success(self):
        from app.adapters.incoming.api.dependencies.tags import add_tag_to_asset_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = make_mock_asset()
        app.dependency_overrides[add_tag_to_asset_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.post(f"/api/v1/assets/{uuid4()}/tags/{uuid4()}")
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.pop(add_tag_to_asset_use_case, None)

    def test_remove_tag_from_asset_success(self):
        from app.adapters.incoming.api.dependencies.tags import remove_tag_from_asset_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = None
        app.dependency_overrides[remove_tag_from_asset_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.delete(f"/api/v1/assets/{uuid4()}/tags/{uuid4()}")
            assert resp.status_code == 204
        finally:
            app.dependency_overrides.pop(remove_tag_from_asset_use_case, None)


class TestPortfolioRouteCoverage:
    def test_delete_portfolio_success(self):
        from app.adapters.incoming.api.dependencies.portfolios import delete_portfolio_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = None
        app.dependency_overrides[delete_portfolio_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.delete(f"/api/v1/portfolios/{uuid4()}")
            assert resp.status_code == 204
        finally:
            app.dependency_overrides.pop(delete_portfolio_use_case, None)

    def test_take_portfolio_snapshot_success(self):
        from app.adapters.incoming.api.dependencies.portfolios import take_portfolio_snapshot_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = make_mock_portfolio_snapshot()
        app.dependency_overrides[take_portfolio_snapshot_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.post(f"/api/v1/portfolios/{uuid4()}/snapshots")
            assert resp.status_code == 201
        finally:
            app.dependency_overrides.pop(take_portfolio_snapshot_use_case, None)

    def test_get_portfolio_snapshots_success(self):
        from app.adapters.incoming.api.dependencies.portfolios import get_portfolio_snapshots_use_case
        mock_uc = MagicMock()
        mock_portfolio = make_mock_portfolio()
        mock_portfolio.snapshots = [make_mock_portfolio_snapshot()]
        mock_uc.execute.return_value = mock_portfolio
        app.dependency_overrides[get_portfolio_snapshots_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.get(f"/api/v1/portfolios/{uuid4()}/snapshots")
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.pop(get_portfolio_snapshots_use_case, None)

    def test_get_all_portfolios_success(self):
        from app.adapters.incoming.api.dependencies.portfolios import get_all_portfolios_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = [make_mock_portfolio()]
        app.dependency_overrides[get_all_portfolios_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.get("/api/v1/portfolios/")
            assert resp.status_code == 200
            assert len(resp.json()) == 1
        finally:
            app.dependency_overrides.pop(get_all_portfolios_use_case, None)


class TestCategoryRouteCoverage:
    def test_get_category_by_id_success(self):
        from app.adapters.incoming.api.dependencies.categories import get_category_use_case
        from app.domain.entities.category import Category
        mock_uc = MagicMock()
        cat = Category(id=uuid4(), name="Stocks")
        mock_uc.execute.return_value = cat
        app.dependency_overrides[get_category_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.get(f"/api/v1/categories/{uuid4()}")
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.pop(get_category_use_case, None)

    def test_assign_asset_to_category_success(self):
        from app.adapters.incoming.api.dependencies.categories import (
            add_asset_to_category_use_case,
            get_category_use_case,
        )
        from app.domain.entities.category import Category
        mock_add_uc = MagicMock()
        mock_get_uc = MagicMock()
        cat = Category(id=uuid4(), name="Stocks")
        mock_add_uc.execute.return_value = None
        mock_get_uc.execute.return_value = cat
        app.dependency_overrides[add_asset_to_category_use_case] = lambda: mock_add_uc
        app.dependency_overrides[get_category_use_case] = lambda: mock_get_uc
        try:
            client = TestClient(app)
            resp = client.post(
                f"/api/v1/categories/{uuid4()}/assets",
                json={"asset_id": str(uuid4())}
            )
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.pop(add_asset_to_category_use_case, None)
            app.dependency_overrides.pop(get_category_use_case, None)

    def test_get_all_categories_success(self):
        from app.adapters.incoming.api.dependencies.categories import get_all_categories_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = []
        app.dependency_overrides[get_all_categories_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.get("/api/v1/categories/")
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.pop(get_all_categories_use_case, None)


class TestTagRouteCoverage:
    def test_get_tag_by_id_success(self):
        from app.adapters.incoming.api.dependencies.tags import get_tag_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = make_mock_tag()
        app.dependency_overrides[get_tag_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.get(f"/api/v1/tags/{uuid4()}")
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.pop(get_tag_use_case, None)

    def test_delete_tag_success(self):
        from app.adapters.incoming.api.dependencies.tags import delete_tag_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = None
        app.dependency_overrides[delete_tag_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.delete(f"/api/v1/tags/{uuid4()}")
            assert resp.status_code == 204
        finally:
            app.dependency_overrides.pop(delete_tag_use_case, None)

    def test_get_all_tags_success(self):
        from app.adapters.incoming.api.dependencies.tags import get_all_tags_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = [make_mock_tag()]
        app.dependency_overrides[get_all_tags_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.get("/api/v1/tags/")
            assert resp.status_code == 200
            assert len(resp.json()) == 1
        finally:
            app.dependency_overrides.pop(get_all_tags_use_case, None)


class TestAssetTypeRouteCoverage:
    def test_get_asset_type_by_id_success(self):
        from app.adapters.incoming.api.dependencies.asset_types import get_asset_type_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = make_mock_asset_type()
        app.dependency_overrides[get_asset_type_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.get(f"/api/v1/asset-types/{uuid4()}")
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.pop(get_asset_type_use_case, None)

    def test_get_all_asset_types_success(self):
        from app.adapters.incoming.api.dependencies.asset_types import get_all_asset_types_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = [make_mock_asset_type()]
        app.dependency_overrides[get_all_asset_types_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.get("/api/v1/asset-types/")
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.pop(get_all_asset_types_use_case, None)


class TestAssetCategoryRouteCoverage:
    def test_add_category_to_asset_success(self):
        from app.adapters.incoming.api.dependencies.categories import add_asset_to_category_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = make_mock_asset()
        app.dependency_overrides[add_asset_to_category_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.post(f"/api/v1/assets/{uuid4()}/categories/{uuid4()}")
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.pop(add_asset_to_category_use_case, None)

    def test_remove_category_from_asset_success(self):
        from app.adapters.incoming.api.dependencies.categories import remove_asset_from_category_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = None
        app.dependency_overrides[remove_asset_from_category_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.delete(f"/api/v1/assets/{uuid4()}/categories/{uuid4()}")
            assert resp.status_code == 204
        finally:
            app.dependency_overrides.pop(remove_asset_from_category_use_case, None)


class TestDependencyFunctionCoverage:
    def test_get_asset_snapshots_use_case_factory(self):
        """Covers asset_snapshots.py line 27."""
        from app.adapters.incoming.api.dependencies.asset_snapshots import get_asset_snapshots_use_case
        from app.application.use_cases.asset_snapshot.get_asset_snapshots import GetAssetSnapshotsUseCase
        mock_snap_repo = MagicMock()
        mock_asset_repo = MagicMock()
        result = get_asset_snapshots_use_case(mock_snap_repo, mock_asset_repo)
        assert isinstance(result, GetAssetSnapshotsUseCase)

    def test_remove_asset_from_category_use_case_factory(self):
        """Covers categories.py line 55."""
        from app.adapters.incoming.api.dependencies.categories import remove_asset_from_category_use_case
        from app.application.use_cases.category.remove_asset_from_category import RemoveAssetFromCategoryUseCase
        mock_asset_repo = MagicMock()
        mock_cat_repo = MagicMock()
        result = remove_asset_from_category_use_case(mock_asset_repo, mock_cat_repo)
        assert isinstance(result, RemoveAssetFromCategoryUseCase)
    def test_get_asset_type_by_id_success(self):
        from app.adapters.incoming.api.dependencies.asset_types import get_asset_type_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = make_mock_asset_type()
        app.dependency_overrides[get_asset_type_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.get(f"/api/v1/asset-types/{uuid4()}")
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.pop(get_asset_type_use_case, None)

    def test_get_all_asset_types_success(self):
        from app.adapters.incoming.api.dependencies.asset_types import get_all_asset_types_use_case
        mock_uc = MagicMock()
        mock_uc.execute.return_value = [make_mock_asset_type()]
        app.dependency_overrides[get_all_asset_types_use_case] = lambda: mock_uc
        try:
            client = TestClient(app)
            resp = client.get("/api/v1/asset-types/")
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.pop(get_all_asset_types_use_case, None)
