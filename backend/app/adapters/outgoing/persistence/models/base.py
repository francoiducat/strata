"""
SQLAlchemy declarative base and common utilities
"""
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

# ✅ Import Base from database.py instead of creating a new one
from ..database import Base


def utc_now() -> datetime:
    """Return current UTC time (timezone-aware)"""
    return datetime.now(timezone.utc)


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now
    )


class AuditMixin:
    """Mixin for audit fields (created_by, updated_by)"""

    created_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="system"
    )

    updated_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="system"
    )


def generate_uuid() -> str:
    """Generate UUID as string"""
    return str(uuid4())