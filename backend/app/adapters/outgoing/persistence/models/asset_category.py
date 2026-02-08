"""
Asset-Category Association Table (Many-to-Many)
"""
from sqlalchemy import Table, Column, String, ForeignKey

from .base import Base


# Asset <-> Category (Many-to-Many)
asset_category = Table(
    "asset_categories",
    Base.metadata,
    Column(
        "asset_id",
        String(36),
        ForeignKey("assets.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "category_id",
        String(36),
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True
    )
)