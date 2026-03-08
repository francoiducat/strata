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
TAG_LIQUID             = '11668c10-673a-41d0-835a-36c1dc9a810e'
TAG_LONG_TERM          = '7e7bfc70-6b27-4a63-a4d4-8c891d6c7f64'
TAG_PRIMARY_RESIDENCE  = '733446e1-f89f-4dc4-a2ab-4a0118da0aae'
TAG_INCOME_GENERATING  = 'ca6c4c87-44c3-4091-85f2-97b973ae1f97'
TAG_INSURED            = 'b1d1d248-e359-4ab0-a071-d49e7056bb17'
TAG_TAX_ADVANTAGED     = 'de3819fc-b521-4220-85a1-8d85ef21750a'
TAG_VINTAGE            = '18d06af3-5db1-4a60-80fb-7a95216a5bd7'
TAG_COLLECTIBLE        = '83ddb16d-46f9-46e4-83ac-104a973a748c'

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
