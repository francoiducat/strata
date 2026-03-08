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
CAT_FINANCIAL_ASSETS   = '205ed564-dfe1-4ecb-befe-1c4275fd549d'
CAT_REAL_ESTATE        = '6297489b-b3db-49b8-aea9-7f8cbbebb105'
CAT_PERSONAL_PROPERTY  = '8f44133e-5404-49e5-a984-4507dccfe9a9'
CAT_COLLECTIONS        = '0f64aff7-dd14-4b10-a31b-b29204ee00d9'
CAT_LIABILITIES        = '899a4cb7-c465-49d4-85a3-410dededd0e1'

# Children of Financial Assets
CAT_CASH_BANKING       = '39bfd491-96e8-4b64-b882-864dd19b5c5b'
CAT_INVESTMENTS        = '937700a0-b24b-4eb8-aaa6-8edb6354a05d'
CAT_CRYPTOCURRENCY     = '65bae68e-d33b-4cca-bb20-cc7a84780143'

# Children of Real Estate
CAT_RESIDENTIAL        = '6dfe992e-dbbd-48b9-816a-886306402ed7'
CAT_COMMERCIAL         = 'dc16d780-c091-49a3-bc3d-d95e2b1d8416'

# Children of Personal Property
CAT_ELECTRONICS_TECH   = '01c12f51-233f-45de-b19e-04ce4331ca86'
CAT_VEHICLES           = '36684648-9dbd-410d-aece-7b3e27539714'
CAT_CLOTHING_FASHION   = '32e9bf97-7c8c-49a5-83c6-7076c62e143a'

# Children of Collections
CAT_ART_ANTIQUES       = 'fb659ba5-68be-4797-abcd-56b033b135aa'
CAT_HOBBIES_SPORTS     = '005b33ba-e438-46c5-81e4-c7c73cd3bc61'

# Children of Liabilities
CAT_LOANS_CREDIT       = '437d744f-2f03-4331-a23d-4ff745418865'
CAT_MORTGAGES          = '4a7e6f5c-d1e3-4b92-9f08-5c2a1d8e7b34'

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
