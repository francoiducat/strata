"""
Asset-Tag Association Table (Many-to-Many)
"""
from sqlalchemy import Table, Column, String, ForeignKey

from .base import Base


# Asset <-> Tag (Many-to-Many)
asset_tag = Table(
    "asset_tags",
    Base.metadata,
    Column(
        "asset_id",
        String(36),
        ForeignKey("assets.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "tag_id",
        String(36),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True
    )
)