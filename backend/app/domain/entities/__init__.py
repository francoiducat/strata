"""
Domain Entities Package

Import all entity classes here in dependency order and call model_rebuild()
to resolve Pydantic v2 forward references (TYPE_CHECKING imports).

This is required because many entities reference each other via string
annotations. model_rebuild() is called after all classes are defined so
Pydantic can resolve every forward ref.
"""

from app.domain.entities.tag import Tag
from app.domain.entities.asset_type import AssetType
from app.domain.entities.transaction import Transaction
from app.domain.entities.category import Category
from app.domain.entities.portfolio_snapshot import PortfolioSnapshot
from app.domain.entities.asset_snapshot import AssetSnapshot
from app.domain.entities.portfolio import Portfolio
from app.domain.entities.asset import Asset

# Resolve all forward references now that every class is in scope.
Tag.model_rebuild()
AssetType.model_rebuild()
Transaction.model_rebuild()
Category.model_rebuild()
PortfolioSnapshot.model_rebuild()
AssetSnapshot.model_rebuild()
Portfolio.model_rebuild()
Asset.model_rebuild()

__all__ = [
    "Tag",
    "AssetType",
    "Transaction",
    "Category",
    "PortfolioSnapshot",
    "AssetSnapshot",
    "Portfolio",
    "Asset",
]
