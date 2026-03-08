"""Tests for ORM models __repr__ methods and base utilities."""
from uuid import uuid4
from datetime import datetime, timezone


def test_tag_model_repr():
    from app.adapters.outgoing.persistence.models.tag import TagModel
    t = TagModel(id=str(uuid4()), name="crypto")
    assert "TagModel" in repr(t)
    assert "crypto" in repr(t)


def test_category_model_repr():
    from app.adapters.outgoing.persistence.models.category import CategoryModel
    c = CategoryModel(id=str(uuid4()), name="Stocks")
    assert "CategoryModel" in repr(c)
    assert "Stocks" in repr(c)


def test_portfolio_model_repr():
    from app.adapters.outgoing.persistence.models.portfolio import PortfolioModel
    now = datetime.now(timezone.utc)
    p = PortfolioModel(id=str(uuid4()), name="My Portfolio", base_currency="EUR", created_at=now, updated_at=now)
    assert "PortfolioModel" in repr(p)
    assert "My Portfolio" in repr(p)


def test_asset_snapshot_model_repr():
    from app.adapters.outgoing.persistence.models.asset_snapshot import AssetSnapshotModel
    from decimal import Decimal
    now = datetime.now(timezone.utc)
    s = AssetSnapshotModel(
        id=str(uuid4()), asset_id=str(uuid4()), value=Decimal("100.0"), observed_at=now
    )
    assert "AssetSnapshotModel" in repr(s)


def test_asset_type_model_repr():
    from app.adapters.outgoing.persistence.models.asset_type import AssetTypeModel
    at = AssetTypeModel(id=str(uuid4()), code="EQUITY", label="Equity")
    assert "AssetTypeModel" in repr(at)
    assert "EQUITY" in repr(at)


def test_portfolio_snapshot_model_repr():
    from app.adapters.outgoing.persistence.models.portfolio_snapshot import PortfolioSnapshotModel
    from decimal import Decimal
    now = datetime.now(timezone.utc)
    s = PortfolioSnapshotModel(
        id=str(uuid4()), portfolio_id=str(uuid4()), value=Decimal("500.0"), observed_at=now
    )
    assert "PortfolioSnapshotModel" in repr(s)


def test_transaction_model_repr():
    from app.adapters.outgoing.persistence.models.transaction import TransactionModel
    from decimal import Decimal
    now = datetime.now(timezone.utc)
    t = TransactionModel(
        id=str(uuid4()), asset_id=str(uuid4()), type="BUY",
        unit_price=Decimal("100.0"), quantity=Decimal("1.0"),
        currency="EUR", occurred_at=now
    )
    assert "TransactionModel" in repr(t)


def test_asset_model_repr():
    from app.adapters.outgoing.persistence.models.asset import AssetModel
    now = datetime.now(timezone.utc)
    a = AssetModel(
        id=str(uuid4()), portfolio_id=str(uuid4()), asset_type_id=str(uuid4()),
        name="Test", created_at=now, updated_at=now, created_by="u", updated_by="u"
    )
    # asset_type not loaded, so code fallback to None
    assert "AssetModel" in repr(a)


def test_generate_uuid():
    from app.adapters.outgoing.persistence.models.base import generate_uuid
    result = generate_uuid()
    assert isinstance(result, str)
    assert len(result) == 36
