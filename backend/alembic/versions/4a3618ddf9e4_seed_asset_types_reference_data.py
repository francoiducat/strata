"""Seed asset types reference data

Revision ID: 4a3618ddf9e4
Revises: 4ec8169a994c
Create Date: 2026-01-25 17:01:10.671566

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from uuid import uuid4
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a3618ddf9e4'
down_revision: Union[str, Sequence[str], None] = '4ec8169a994c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Asset types reference data
ASSET_TYPES = [
    {'code': 'CASH', 'label': 'Cash'},
    {'code': 'CHECKING_ACCOUNT', 'label': 'Checking Account'},
    {'code': 'SAVINGS_ACCOUNT', 'label': 'Savings Account'},
    {'code': 'REAL_ESTATE', 'label': 'Real Estate'},
    {'code': 'STOCKS', 'label': 'Stocks & Funds'},
    {'code': 'BONDS', 'label': 'Bonds'},
    {'code': 'CRYPTO', 'label': 'Cryptocurrency'},
    {'code': 'COMMODITIES', 'label': 'Commodities'},
    {'code': 'PERSONAL_PROPERTY', 'label': 'Personal Property'},
    {'code': 'COLLECTIBLES', 'label': 'Collectibles'},
    {'code': 'BUSINESS_OWNERSHIP', 'label': 'Business Ownership'},
    {'code': 'LOAN', 'label': 'Loan (Liability)'},
    {'code': 'CREDIT_CARD', 'label': 'Credit Card (Liability)'},
    {'code': 'MORTGAGE', 'label': 'Mortgage (Liability)'},
    {'code': 'OTHER', 'label': 'Other'},
]


def upgrade() -> None:
    """Insert asset types reference data"""

    now = datetime.now(timezone.utc)

    # Prepare data for bulk insert
    data = [
        {
            'id': str(uuid4()),
            'code': at['code'],
            'label': at['label'],
            'created_at': now,
            'updated_at': now,
        }
        for at in ASSET_TYPES
    ]

    # Bulk insert using op.bulk_insert
    asset_types_table = sa.table(
        'asset_types',
        sa.column('id', sa.String),
        sa.column('code', sa.String),
        sa.column('label', sa.String),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime),
    )

    op.bulk_insert(asset_types_table, data)

    print(f"✅ Seeded {len(ASSET_TYPES)} asset types")


def downgrade() -> None:
    """Remove seeded asset types"""

    # Delete only the asset types we inserted
    codes = [at['code'] for at in ASSET_TYPES]

    op.execute(
        sa.text(
            "DELETE FROM asset_types WHERE code IN :codes"
        ).bindparams(
            codes=tuple(codes)
        )
    )

    print(f"✅ Removed {len(ASSET_TYPES)} asset types")
