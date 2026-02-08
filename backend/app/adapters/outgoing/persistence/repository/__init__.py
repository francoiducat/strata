"""
Repository Implementations (SQLAlchemy Adapters)

Export all repository implementations. Imports are guarded so that
missing or empty implementation modules don't cause import-time errors
(e.g., during incremental development).
"""

from .sqlalchemy_portfolio_repository import SQLAlchemyPortfolioRepository
from .sqlalchemy_asset_repository import SQLAlchemyAssetRepository
from .sqlalchemy_asset_type_repository import SQLAlchemyAssetTypeRepository
from .sqlalchemy_category_repository import SQLAlchemyCategoryRepository
from .sqlalchemy_portfolio_snapshot_repository import SQLAlchemyPortfolioSnapshotRepository
from .sqlalchemy_asset_snapshot_repository import SQLAlchemyAssetSnapshotRepository
from .sqlalchemy_transaction_repository import SQLAlchemyTransactionRepository
from .sqlalchemy_tag_repository import SQLAlchemyTagRepository

__all__ = [
    "SQLAlchemyPortfolioRepository",
    "SQLAlchemyAssetRepository",
    "SQLAlchemyAssetTypeRepository",
    "SQLAlchemyCategoryRepository",
    "SQLAlchemyPortfolioSnapshotRepository",
    "SQLAlchemyAssetSnapshotRepository",
    "SQLAlchemyTransactionRepository",
    "SQLAlchemyTagRepository",
]
