"""Seed categories reference data

Revision ID: a1b2c3d4e5f6
Revises: 4a3618ddf9e4
Create Date: 2026-01-26 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '4a3618ddf9e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Fixed UUIDs for idempotent downgrade
# Roots
CAT_FINANCIAL_ASSETS   = 'c0000001-0000-0000-0000-000000000001'
CAT_REAL_ESTATE        = 'c0000001-0000-0000-0000-000000000002'
CAT_PERSONAL_PROPERTY  = 'c0000001-0000-0000-0000-000000000003'
CAT_COLLECTIONS        = 'c0000001-0000-0000-0000-000000000004'
CAT_LIABILITIES        = 'c0000001-0000-0000-0000-000000000005'

# Children of Financial Assets
CAT_CASH_BANKING       = 'c0000001-0000-0000-0000-000000000011'
CAT_INVESTMENTS        = 'c0000001-0000-0000-0000-000000000012'
CAT_CRYPTOCURRENCY     = 'c0000001-0000-0000-0000-000000000013'

# Children of Real Estate
CAT_RESIDENTIAL        = 'c0000001-0000-0000-0000-000000000021'
CAT_COMMERCIAL         = 'c0000001-0000-0000-0000-000000000022'

# Children of Personal Property
CAT_ELECTRONICS_TECH   = 'c0000001-0000-0000-0000-000000000031'
CAT_VEHICLES           = 'c0000001-0000-0000-0000-000000000032'
CAT_CLOTHING_FASHION   = 'c0000001-0000-0000-0000-000000000033'

# Children of Collections
CAT_ART_ANTIQUES       = 'c0000001-0000-0000-0000-000000000041'
CAT_HOBBIES_SPORTS     = 'c0000001-0000-0000-0000-000000000042'

# Children of Liabilities
CAT_LOANS_CREDIT       = 'c0000001-0000-0000-0000-000000000051'
CAT_MORTGAGES          = 'c0000001-0000-0000-0000-000000000052'

ALL_CATEGORY_IDS = [
    CAT_FINANCIAL_ASSETS, CAT_REAL_ESTATE, CAT_PERSONAL_PROPERTY,
    CAT_COLLECTIONS, CAT_LIABILITIES,
    CAT_CASH_BANKING, CAT_INVESTMENTS, CAT_CRYPTOCURRENCY,
    CAT_RESIDENTIAL, CAT_COMMERCIAL,
    CAT_ELECTRONICS_TECH, CAT_VEHICLES, CAT_CLOTHING_FASHION,
    CAT_ART_ANTIQUES, CAT_HOBBIES_SPORTS,
    CAT_LOANS_CREDIT, CAT_MORTGAGES,
]


def upgrade() -> None:
    """Insert 5 root categories and 12 child categories"""

    categories_table = sa.table(
        'categories',
        sa.column('id', sa.String),
        sa.column('name', sa.String),
        sa.column('parent_id', sa.String),
    )

    # Insert roots first (no parent_id)
    roots = [
        {'id': CAT_FINANCIAL_ASSETS,  'name': 'Financial Assets',   'parent_id': None},
        {'id': CAT_REAL_ESTATE,       'name': 'Real Estate',        'parent_id': None},
        {'id': CAT_PERSONAL_PROPERTY, 'name': 'Personal Property',  'parent_id': None},
        {'id': CAT_COLLECTIONS,       'name': 'Collections',        'parent_id': None},
        {'id': CAT_LIABILITIES,       'name': 'Liabilities',        'parent_id': None},
    ]
    op.bulk_insert(categories_table, roots)

    # Insert children (reference parent_id set above)
    children = [
        {'id': CAT_CASH_BANKING,      'name': 'Cash & Banking',       'parent_id': CAT_FINANCIAL_ASSETS},
        {'id': CAT_INVESTMENTS,       'name': 'Investments',           'parent_id': CAT_FINANCIAL_ASSETS},
        {'id': CAT_CRYPTOCURRENCY,    'name': 'Cryptocurrency',        'parent_id': CAT_FINANCIAL_ASSETS},
        {'id': CAT_RESIDENTIAL,       'name': 'Residential',           'parent_id': CAT_REAL_ESTATE},
        {'id': CAT_COMMERCIAL,        'name': 'Commercial',            'parent_id': CAT_REAL_ESTATE},
        {'id': CAT_ELECTRONICS_TECH,  'name': 'Electronics & Tech',    'parent_id': CAT_PERSONAL_PROPERTY},
        {'id': CAT_VEHICLES,          'name': 'Vehicles',              'parent_id': CAT_PERSONAL_PROPERTY},
        {'id': CAT_CLOTHING_FASHION,  'name': 'Clothing & Fashion',    'parent_id': CAT_PERSONAL_PROPERTY},
        {'id': CAT_ART_ANTIQUES,      'name': 'Art & Antiques',        'parent_id': CAT_COLLECTIONS},
        {'id': CAT_HOBBIES_SPORTS,    'name': 'Hobbies & Sports',      'parent_id': CAT_COLLECTIONS},
        {'id': CAT_LOANS_CREDIT,      'name': 'Loans & Credit',        'parent_id': CAT_LIABILITIES},
        {'id': CAT_MORTGAGES,         'name': 'Mortgages',             'parent_id': CAT_LIABILITIES},
    ]
    op.bulk_insert(categories_table, children)

    print(f"✅ Seeded {len(roots)} root categories and {len(children)} child categories")


def downgrade() -> None:
    """Remove seeded categories (children before roots to respect FK)"""

    ids_clause = ','.join(f"'{id}'" for id in ALL_CATEGORY_IDS)
    op.execute(sa.text(f"DELETE FROM categories WHERE id IN ({ids_clause})"))

    print(f"✅ Removed {len(ALL_CATEGORY_IDS)} categories")
