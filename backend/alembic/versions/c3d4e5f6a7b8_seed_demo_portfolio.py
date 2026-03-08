"""Seed demo portfolio with assets, categories and tags

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-01-26 10:02:00.000000

"""
from typing import Sequence, Union
from datetime import datetime, timezone
from decimal import Decimal
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, Sequence[str], None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ---------------------------------------------------------------------------
# Fixed UUIDs (all module-level so downgrade() can delete by known IDs)
# ---------------------------------------------------------------------------

# Portfolio
PORTFOLIO_ID = 'fea54085-57b9-41ba-9f22-3012c5fa40d8'

# Assets
ASSET_CHECKING   = 'e1136fa0-02bb-4720-9314-683485b4e2ee'
ASSET_SAVINGS    = '6540125c-ac5c-43e5-8091-f52bd86c8a91'
ASSET_STOCKS     = '68f27860-8552-408f-92bb-98d7e71de783'
ASSET_BITCOIN    = 'b8457fa8-6ac7-460e-ae1f-0d7d33a68ec3'
ASSET_RESIDENCE  = 'f136feb4-7ac3-47b4-990c-21d04dac0417'
ASSET_CAR        = 'c6d87a34-39a9-48f9-81b4-8b2191ad9b3d'
ASSET_MORTGAGE   = '47dc7c65-b3ba-4c62-a274-48c7161d85d5'
ASSET_CAR_LOAN   = '95b3bcac-3db1-41db-9d7c-aadb71df1b09'

ALL_ASSET_IDS = [
    ASSET_CHECKING, ASSET_SAVINGS, ASSET_STOCKS, ASSET_BITCOIN,
    ASSET_RESIDENCE, ASSET_CAR, ASSET_MORTGAGE, ASSET_CAR_LOAN,
]

# Category UUIDs (from seed_categories migration — must stay in sync)
CAT_FINANCIAL_ASSETS   = '205ed564-dfe1-4ecb-befe-1c4275fd549d'
CAT_REAL_ESTATE        = '6297489b-b3db-49b8-aea9-7f8cbbebb105'
CAT_PERSONAL_PROPERTY  = '8f44133e-5404-49e5-a984-4507dccfe9a9'
CAT_LIABILITIES        = '899a4cb7-c465-49d4-85a3-410dededd0e1'
CAT_CASH_BANKING       = '39bfd491-96e8-4b64-b882-864dd19b5c5b'
CAT_INVESTMENTS        = '937700a0-b24b-4eb8-aaa6-8edb6354a05d'
CAT_CRYPTOCURRENCY     = '65bae68e-d33b-4cca-bb20-cc7a84780143'
CAT_RESIDENTIAL        = '6dfe992e-dbbd-48b9-816a-886306402ed7'
CAT_VEHICLES           = '36684648-9dbd-410d-aece-7b3e27539714'
CAT_LOANS_CREDIT       = '437d744f-2f03-4331-a23d-4ff745418865'
CAT_MORTGAGES          = '4a7e6f5c-d1e3-4b92-9f08-5c2a1d8e7b34'

# Tag UUIDs (from seed_tags migration — must stay in sync)
TAG_LIQUID             = '11668c10-673a-41d0-835a-36c1dc9a810e'
TAG_LONG_TERM          = '7e7bfc70-6b27-4a63-a4d4-8c891d6c7f64'
TAG_PRIMARY_RESIDENCE  = '733446e1-f89f-4dc4-a2ab-4a0118da0aae'
TAG_INSURED            = 'b1d1d248-e359-4ab0-a071-d49e7056bb17'
TAG_TAX_ADVANTAGED     = 'de3819fc-b521-4220-85a1-8d85ef21750a'


def upgrade() -> None:
    """
    Seed a demo portfolio with 8 assets, 16 category assignments, and
    8 tag assignments. No snapshots are included — the user will create
    their first snapshot from the front-end app.
    """

    now = datetime.now(timezone.utc)

    # ------------------------------------------------------------------
    # Resolve asset_type_id by code at runtime
    # ------------------------------------------------------------------
    bind = op.get_bind()
    rows = bind.execute(sa.text("SELECT id, code FROM asset_types")).fetchall()
    asset_type_id = {row.code: row.id for row in rows}

    # ------------------------------------------------------------------
    # 1. Portfolio
    # ------------------------------------------------------------------
    portfolios_table = sa.table(
        'portfolios',
        sa.column('id', sa.String),
        sa.column('name', sa.String),
        sa.column('base_currency', sa.String),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime),
    )
    op.bulk_insert(portfolios_table, [
        {
            'id': PORTFOLIO_ID,
            'name': 'My Portfolio',
            'base_currency': 'EUR',
            'created_at': now,
            'updated_at': now,
        }
    ])

    # ------------------------------------------------------------------
    # 2. Assets (8 rows)
    # ------------------------------------------------------------------
    assets_table = sa.table(
        'assets',
        sa.column('id', sa.String),
        sa.column('portfolio_id', sa.String),
        sa.column('asset_type_id', sa.String),
        sa.column('name', sa.String),
        sa.column('quantity', sa.Numeric),
        sa.column('disposed', sa.Boolean),
        sa.column('created_by', sa.String),
        sa.column('updated_by', sa.String),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime),
    )

    def _asset(asset_id, type_code, name, quantity=None):
        return {
            'id': asset_id,
            'portfolio_id': PORTFOLIO_ID,
            'asset_type_id': asset_type_id[type_code],
            'name': name,
            'quantity': quantity,
            'disposed': False,
            'created_by': 'seed',
            'updated_by': 'seed',
            'created_at': now,
            'updated_at': now,
        }

    op.bulk_insert(assets_table, [
        _asset(ASSET_CHECKING,  'CHECKING_ACCOUNT', 'Main Checking Account'),
        _asset(ASSET_SAVINGS,   'SAVINGS_ACCOUNT',  'Savings Account'),
        _asset(ASSET_STOCKS,    'STOCKS',           'Stock Portfolio',         quantity=Decimal('100.0')),
        _asset(ASSET_BITCOIN,   'CRYPTO',           'Bitcoin',                 quantity=Decimal('0.05')),
        _asset(ASSET_RESIDENCE, 'REAL_ESTATE',      'Primary Residence',       quantity=Decimal('1.0')),
        _asset(ASSET_CAR,       'PERSONAL_PROPERTY','Car',                     quantity=Decimal('1.0')),
        _asset(ASSET_MORTGAGE,  'MORTGAGE',         'Home Mortgage'),
        _asset(ASSET_CAR_LOAN,  'LOAN',             'Car Loan'),
    ])

    # ------------------------------------------------------------------
    # 3. Asset categories (16 rows — root + leaf per asset)
    # ------------------------------------------------------------------
    asset_categories_table = sa.table(
        'asset_categories',
        sa.column('asset_id', sa.String),
        sa.column('category_id', sa.String),
    )
    op.bulk_insert(asset_categories_table, [
        {'asset_id': ASSET_CHECKING,  'category_id': CAT_FINANCIAL_ASSETS},
        {'asset_id': ASSET_CHECKING,  'category_id': CAT_CASH_BANKING},
        {'asset_id': ASSET_SAVINGS,   'category_id': CAT_FINANCIAL_ASSETS},
        {'asset_id': ASSET_SAVINGS,   'category_id': CAT_CASH_BANKING},
        {'asset_id': ASSET_STOCKS,    'category_id': CAT_FINANCIAL_ASSETS},
        {'asset_id': ASSET_STOCKS,    'category_id': CAT_INVESTMENTS},
        {'asset_id': ASSET_BITCOIN,   'category_id': CAT_FINANCIAL_ASSETS},
        {'asset_id': ASSET_BITCOIN,   'category_id': CAT_CRYPTOCURRENCY},
        {'asset_id': ASSET_RESIDENCE, 'category_id': CAT_REAL_ESTATE},
        {'asset_id': ASSET_RESIDENCE, 'category_id': CAT_RESIDENTIAL},
        {'asset_id': ASSET_CAR,       'category_id': CAT_PERSONAL_PROPERTY},
        {'asset_id': ASSET_CAR,       'category_id': CAT_VEHICLES},
        {'asset_id': ASSET_MORTGAGE,  'category_id': CAT_LIABILITIES},
        {'asset_id': ASSET_MORTGAGE,  'category_id': CAT_MORTGAGES},
        {'asset_id': ASSET_CAR_LOAN,  'category_id': CAT_LIABILITIES},
        {'asset_id': ASSET_CAR_LOAN,  'category_id': CAT_LOANS_CREDIT},
    ])

    # ------------------------------------------------------------------
    # 4. Asset tags (8 rows)
    # ------------------------------------------------------------------
    asset_tags_table = sa.table(
        'asset_tags',
        sa.column('asset_id', sa.String),
        sa.column('tag_id', sa.String),
    )
    op.bulk_insert(asset_tags_table, [
        {'asset_id': ASSET_CHECKING,  'tag_id': TAG_LIQUID},
        {'asset_id': ASSET_SAVINGS,   'tag_id': TAG_LIQUID},
        {'asset_id': ASSET_STOCKS,    'tag_id': TAG_LONG_TERM},
        {'asset_id': ASSET_STOCKS,    'tag_id': TAG_TAX_ADVANTAGED},
        {'asset_id': ASSET_BITCOIN,   'tag_id': TAG_LONG_TERM},
        {'asset_id': ASSET_RESIDENCE, 'tag_id': TAG_PRIMARY_RESIDENCE},
        {'asset_id': ASSET_RESIDENCE, 'tag_id': TAG_INSURED},
        {'asset_id': ASSET_CAR,       'tag_id': TAG_INSURED},
    ])

    print(f"✅ Seeded demo portfolio '{PORTFOLIO_ID}' with {len(ALL_ASSET_IDS)} assets")


def downgrade() -> None:
    """Remove all seeded demo data in reverse FK order."""

    bind = op.get_bind()

    # asset_tags
    assets_clause = ','.join(f"'{id}'" for id in ALL_ASSET_IDS)
    bind.execute(sa.text(f"DELETE FROM asset_tags WHERE asset_id IN ({assets_clause})"))

    # asset_categories
    bind.execute(sa.text(f"DELETE FROM asset_categories WHERE asset_id IN ({assets_clause})"))

    # assets
    bind.execute(sa.text(f"DELETE FROM assets WHERE id IN ({assets_clause})"))

    # portfolio
    bind.execute(sa.text(f"DELETE FROM portfolios WHERE id = '{PORTFOLIO_ID}'"))

    print("✅ Removed demo portfolio and all related data")
