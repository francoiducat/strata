"""
SQLAlchemy Models Package

Import all models here to ensure they're registered with SQLAlchemy Base
"""
from .base import Base

# Import association tables FIRST (before models that use them)
from .asset_category import asset_category
from .asset_tag import asset_tag

# Then import models
from .portfolio import PortfolioModel
from .asset_type import AssetTypeModel
from .category import CategoryModel
from .tag import TagModel
from .asset import AssetModel
from .transaction import TransactionModel
from .asset_snapshot import AssetSnapshotModel
from .portfolio_snapshot import PortfolioSnapshotModel

__all__ = [
    "Base",
    "PortfolioModel",
    "AssetTypeModel",
    "CategoryModel",
    "TagModel",
    "AssetModel",
    "TransactionModel",
    "AssetSnapshotModel",
    "PortfolioSnapshotModel",
    "asset_category",
    "asset_tag",
]