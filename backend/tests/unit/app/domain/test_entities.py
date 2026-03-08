"""Unit tests for domain entities."""
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest

from app.domain.entities.asset import Asset
from app.domain.entities.asset_snapshot import AssetSnapshot
from app.domain.entities.asset_type import AssetType
from app.domain.entities.category import Category
from app.domain.entities.portfolio import Portfolio
from app.domain.entities.portfolio_snapshot import PortfolioSnapshot
from app.domain.entities.tag import Tag


def _now():
    return datetime.now(timezone.utc)


def make_portfolio():
    return Portfolio(
        id=uuid4(), name="Test", base_currency="EUR",
        created_at=_now(), updated_at=_now()
    )


def make_asset_type():
    return AssetType(id=uuid4(), code="EQUITY", label="Equity")


def make_asset(portfolio=None, snapshots=None):
    return Asset(
        id=uuid4(), name="My Asset",
        asset_type=make_asset_type(),
        portfolio=portfolio or make_portfolio(),
        snapshots=snapshots or [],
        created_at=_now(), updated_at=_now(),
        created_by="user", updated_by="user",
    )


def make_snapshot(asset_id, value, observed_at=None):
    return AssetSnapshot(
        id=uuid4(), asset_id=asset_id,
        value=Decimal(str(value)),
        observed_at=observed_at or _now(),
    )


# ---------------------------------------------------------------------------
# Asset entity tests
# ---------------------------------------------------------------------------

class TestAssetCurrentValue:
    def test_no_snapshots_returns_zero(self):
        asset = make_asset()
        assert asset.current_value() == Decimal("0.0")

    def test_returns_latest_snapshot_value(self):
        asset_id = uuid4()
        s1 = make_snapshot(asset_id, 100, datetime(2024, 1, 1, tzinfo=timezone.utc))
        s2 = make_snapshot(asset_id, 200, datetime(2024, 6, 1, tzinfo=timezone.utc))
        # snapshots assumed sorted descending
        asset = make_asset(snapshots=[s2, s1])
        assert asset.current_value() == Decimal("200")

    def test_with_at_parameter_finds_latest_before_date(self):
        asset_id = uuid4()
        s1 = make_snapshot(asset_id, 100, datetime(2024, 1, 1, tzinfo=timezone.utc))
        s2 = make_snapshot(asset_id, 200, datetime(2024, 6, 1, tzinfo=timezone.utc))
        asset = make_asset(snapshots=[s2, s1])
        at = datetime(2024, 3, 1, tzinfo=timezone.utc)
        assert asset.current_value(at=at) == Decimal("100")


class TestAssetDispose:
    def test_dispose_sets_disposed_true(self):
        asset = make_asset()
        assert not asset.disposed
        asset.dispose()
        assert asset.disposed

    def test_dispose_with_datetime(self):
        asset = make_asset()
        ts = datetime(2024, 5, 1, tzinfo=timezone.utc)
        asset.dispose(at=ts)
        assert asset.disposed
        assert asset.updated_at == ts


class TestAssetCategories:
    def test_add_category(self):
        asset = make_asset()
        cat = Category(id=uuid4(), name="Bonds")
        asset.add_category(cat)
        assert cat in asset.categories

    def test_remove_category(self):
        asset = make_asset()
        cat = Category(id=uuid4(), name="Bonds")
        asset.add_category(cat)
        asset.remove_category(cat)
        assert cat not in asset.categories

    def test_remove_nonexistent_category_is_noop(self):
        asset = make_asset()
        cat = Category(id=uuid4(), name="Missing")
        asset.remove_category(cat)  # should not raise


# ---------------------------------------------------------------------------
# Category entity tests
# ---------------------------------------------------------------------------

class TestCategoryEquality:
    def test_equal_categories(self):
        cid = uuid4()
        c1 = Category(id=cid, name="A")
        c2 = Category(id=cid, name="B")
        assert c1 == c2

    def test_unequal_categories(self):
        c1 = Category(id=uuid4(), name="A")
        c2 = Category(id=uuid4(), name="A")
        assert c1 != c2

    def test_not_equal_to_other_type(self):
        c1 = Category(id=uuid4(), name="A")
        assert c1 != "not a category"


class TestCategoryGetHierarchy:
    def test_single_category(self):
        c = Category(id=uuid4(), name="Root")
        hierarchy = c.get_hierarchy()
        assert hierarchy == [c]

    def test_with_parent_chain(self):
        root = Category(id=uuid4(), name="Root")
        mid = Category(id=uuid4(), name="Mid", parent=root)
        leaf = Category(id=uuid4(), name="Leaf", parent=mid)
        hierarchy = leaf.get_hierarchy()
        assert hierarchy == [leaf, mid, root]


class TestCategoryGetAllAssets:
    def test_flat_returns_own_assets(self):
        asset = make_asset()
        cat = Category(id=uuid4(), name="Stocks", assets=[asset])
        result = cat.get_all_assets()
        assert len(result) == 1
        assert result[0].id == asset.id

    def test_with_children_recursion(self):
        child_asset = make_asset()
        parent_asset = make_asset()
        child = Category(id=uuid4(), name="Child", assets=[child_asset])
        parent = Category(id=uuid4(), name="Parent", assets=[parent_asset], children=[child])
        result = parent.get_all_assets()
        ids = {a.id for a in result}
        assert child_asset.id in ids
        assert parent_asset.id in ids

    def test_deduplicates_assets(self):
        asset = make_asset()
        child = Category(id=uuid4(), name="Child", assets=[asset])
        parent = Category(id=uuid4(), name="Parent", assets=[asset], children=[child])
        result = parent.get_all_assets()
        assert len(result) == 1


# ---------------------------------------------------------------------------
# Tag entity tests
# ---------------------------------------------------------------------------

class TestTagEquality:
    def test_equal_tags(self):
        tid = uuid4()
        t1 = Tag(id=tid, name="green")
        t2 = Tag(id=tid, name="red")
        assert t1 == t2

    def test_unequal_tags(self):
        t1 = Tag(id=uuid4(), name="A")
        t2 = Tag(id=uuid4(), name="A")
        assert t1 != t2

    def test_not_equal_to_other_type(self):
        t = Tag(id=uuid4(), name="A")
        assert t != "not a tag"
        assert t != 42


# ---------------------------------------------------------------------------
# AssetSnapshot entity tests
# ---------------------------------------------------------------------------

class TestAssetSnapshotGetCurrency:
    def test_raises_when_asset_is_none(self):
        snap = AssetSnapshot(id=uuid4(), asset_id=uuid4(), value=Decimal("10"), observed_at=_now())
        with pytest.raises(ValueError, match="Asset back-reference"):
            snap.get_currency()

    def test_returns_portfolio_currency(self):
        portfolio = make_portfolio()
        portfolio.base_currency = "USD"
        asset = make_asset(portfolio=portfolio)
        snap = AssetSnapshot(id=uuid4(), asset_id=asset.id, value=Decimal("10"), observed_at=_now())
        snap.asset = asset
        assert snap.get_currency() == "USD"


# ---------------------------------------------------------------------------
# PortfolioSnapshot entity tests
# ---------------------------------------------------------------------------

class TestPortfolioSnapshotGetCurrency:
    def test_raises_when_portfolio_is_none(self):
        snap = PortfolioSnapshot(
            id=uuid4(), portfolio_id=uuid4(), value=Decimal("100"), observed_at=_now()
        )
        with pytest.raises(ValueError, match="Portfolio back-reference"):
            snap.get_currency()

    def test_returns_portfolio_currency(self):
        portfolio = make_portfolio()
        portfolio.base_currency = "GBP"
        snap = PortfolioSnapshot(
            id=uuid4(), portfolio_id=portfolio.id, value=Decimal("100"), observed_at=_now()
        )
        snap.portfolio = portfolio
        assert snap.get_currency() == "GBP"
