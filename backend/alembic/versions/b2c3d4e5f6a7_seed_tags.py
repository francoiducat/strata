"""Seed tags reference data

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-01-26 10:01:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Fixed UUIDs for idempotent downgrade
TAG_LIQUID             = 'f1000001-0000-0000-0000-000000000001'
TAG_LONG_TERM          = 'f1000001-0000-0000-0000-000000000002'
TAG_PRIMARY_RESIDENCE  = 'f1000001-0000-0000-0000-000000000003'
TAG_INCOME_GENERATING  = 'f1000001-0000-0000-0000-000000000004'
TAG_INSURED            = 'f1000001-0000-0000-0000-000000000005'
TAG_TAX_ADVANTAGED     = 'f1000001-0000-0000-0000-000000000006'
TAG_VINTAGE            = 'f1000001-0000-0000-0000-000000000007'
TAG_COLLECTIBLE        = 'f1000001-0000-0000-0000-000000000008'

ALL_TAG_IDS = [
    TAG_LIQUID, TAG_LONG_TERM, TAG_PRIMARY_RESIDENCE, TAG_INCOME_GENERATING,
    TAG_INSURED, TAG_TAX_ADVANTAGED, TAG_VINTAGE, TAG_COLLECTIBLE,
]

TAGS = [
    {'id': TAG_LIQUID,            'name': 'liquid'},
    {'id': TAG_LONG_TERM,         'name': 'long-term'},
    {'id': TAG_PRIMARY_RESIDENCE, 'name': 'primary-residence'},
    {'id': TAG_INCOME_GENERATING, 'name': 'income-generating'},
    {'id': TAG_INSURED,           'name': 'insured'},
    {'id': TAG_TAX_ADVANTAGED,    'name': 'tax-advantaged'},
    {'id': TAG_VINTAGE,           'name': 'vintage'},
    {'id': TAG_COLLECTIBLE,       'name': 'collectible'},
]


def upgrade() -> None:
    """Insert 8 flat tags"""

    tags_table = sa.table(
        'tags',
        sa.column('id', sa.String),
        sa.column('name', sa.String),
    )

    data = [{'id': tag['id'], 'name': tag['name']} for tag in TAGS]
    op.bulk_insert(tags_table, data)

    print(f"✅ Seeded {len(TAGS)} tags")


def downgrade() -> None:
    """Remove seeded tags"""

    ids_clause = ','.join(f"'{id}'" for id in ALL_TAG_IDS)
    op.execute(sa.text(f"DELETE FROM tags WHERE id IN ({ids_clause})"))

    print(f"✅ Removed {len(ALL_TAG_IDS)} tags")
