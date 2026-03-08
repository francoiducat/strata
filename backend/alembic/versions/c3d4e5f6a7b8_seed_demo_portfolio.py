"""Seed demo portfolio with assets, snapshots and net worth

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
PORTFOLIO_ID = 'e1000001-0000-0000-0000-000000000001'

# Assets
ASSET_CHECKING   = 'a1000001-0000-0000-0000-000000000001'
ASSET_SAVINGS    = 'a1000001-0000-0000-0000-000000000002'
ASSET_STOCKS     = 'a1000001-0000-0000-0000-000000000003'
ASSET_BITCOIN    = 'a1000001-0000-0000-0000-000000000004'
ASSET_RESIDENCE  = 'a1000001-0000-0000-0000-000000000005'
ASSET_CAR        = 'a1000001-0000-0000-0000-000000000006'
ASSET_MORTGAGE   = 'a1000001-0000-0000-0000-000000000007'
ASSET_CAR_LOAN   = 'a1000001-0000-0000-0000-000000000008'

ALL_ASSET_IDS = [
    ASSET_CHECKING, ASSET_SAVINGS, ASSET_STOCKS, ASSET_BITCOIN,
    ASSET_RESIDENCE, ASSET_CAR, ASSET_MORTGAGE, ASSET_CAR_LOAN,
]

# Asset snapshots
SNAP_CHECKING   = 'b1000001-0000-0000-0000-000000000001'
SNAP_SAVINGS    = 'b1000001-0000-0000-0000-000000000002'
SNAP_STOCKS     = 'b1000001-0000-0000-0000-000000000003'
SNAP_BITCOIN    = 'b1000001-0000-0000-0000-000000000004'
SNAP_RESIDENCE  = 'b1000001-0000-0000-0000-000000000005'
SNAP_CAR        = 'b1000001-0000-0000-0000-000000000006'
SNAP_MORTGAGE   = 'b1000001-0000-0000-0000-000000000007'
SNAP_CAR_LOAN   = 'b1000001-0000-0000-0000-000000000008'

ALL_SNAPSHOT_IDS = [
    SNAP_CHECKING, SNAP_SAVINGS, SNAP_STOCKS, SNAP_BITCOIN,
    SNAP_RESIDENCE, SNAP_CAR, SNAP_MORTGAGE, SNAP_CAR_LOAN,
]

# Portfolio snapshot
PORTFOLIO_SNAP_ID = 'd1000001-0000-0000-0000-000000000001'

# Category UUIDs (from seed_categories migration)
CAT_FINANCIAL_ASSETS   = 'c0000001-0000-0000-0000-000000000001'
CAT_REAL_ESTATE        = 'c0000001-0000-0000-0000-000000000002'
CAT_PERSONAL_PROPERTY  = 'c0000001-0000-0000-0000-000000000003'
CAT_LIABILITIES        = 'c0000001-0000-0000-0000-000000000005'
CAT_CASH_BANKING       = 'c0000001-0000-0000-0000-000000000011'
CAT_INVESTMENTS        = 'c0000001-0000-0000-0000-000000000012'
CAT_CRYPTOCURRENCY     = 'c0000001-0000-0000-0000-000000000013'
CAT_RESIDENTIAL        = 'c0000001-0000-0000-0000-000000000021'
CAT_VEHICLES           = 'c0000001-0000-0000-0000-000000000032'
CAT_LOANS_CREDIT       = 'c0000001-0000-0000-0000-000000000051'
CAT_MORTGAGES          = 'c0000001-0000-0000-0000-000000000052'

# Tag UUIDs (from seed_tags migration)
TAG_LIQUID             = 'f1000001-0000-0000-0000-000000000001'
TAG_LONG_TERM          = 'f1000001-0000-0000-0000-000000000002'
TAG_PRIMARY_RESIDENCE  = 'f1000001-0000-0000-0000-000000000003'
TAG_INSURED            = 'f1000001-0000-0000-0000-000000000005'
TAG_TAX_ADVANTAGED     = 'f1000001-0000-0000-0000-000000000006'

# Net worth = 5000 + 15000 + 25000 + 3500 + 350000 + 18000 − 220000 − 8000 = 188500
PORTFOLIO_NET_WORTH = Decimal('188500.00')


def upgrade() -> None:
    """
    Seed a demo portfolio with 8 assets, 8 asset snapshots,
    16 category assignments, 8 tag assignments, and 1 portfolio snapshot.

    All values are in EUR.
    Liabilities use negative snapshot values (reduce net worth per PRD).
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

    # ------------------------------------------------------------------
    # 5. Asset snapshots (8 rows — liabilities are negative values)
    # ------------------------------------------------------------------
    asset_snapshots_table = sa.table(
        'asset_snapshots',
        sa.column('id', sa.String),
        sa.column('asset_id', sa.String),
        sa.column('value', sa.Numeric),
        sa.column('observed_at', sa.DateTime),
    )
    op.bulk_insert(asset_snapshots_table, [
        {'id': SNAP_CHECKING,  'asset_id': ASSET_CHECKING,  'value': Decimal('5000.00'),    'observed_at': now},
        {'id': SNAP_SAVINGS,   'asset_id': ASSET_SAVINGS,   'value': Decimal('15000.00'),   'observed_at': now},
        {'id': SNAP_STOCKS,    'asset_id': ASSET_STOCKS,    'value': Decimal('25000.00'),   'observed_at': now},
        {'id': SNAP_BITCOIN,   'asset_id': ASSET_BITCOIN,   'value': Decimal('3500.00'),    'observed_at': now},
        {'id': SNAP_RESIDENCE, 'asset_id': ASSET_RESIDENCE, 'value': Decimal('350000.00'),  'observed_at': now},
        {'id': SNAP_CAR,       'asset_id': ASSET_CAR,       'value': Decimal('18000.00'),   'observed_at': now},
        {'id': SNAP_MORTGAGE,  'asset_id': ASSET_MORTGAGE,  'value': Decimal('-220000.00'), 'observed_at': now},
        {'id': SNAP_CAR_LOAN,  'asset_id': ASSET_CAR_LOAN,  'value': Decimal('-8000.00'),   'observed_at': now},
    ])

    # ------------------------------------------------------------------
    # 6. Portfolio snapshot (1 row — pre-calculated net worth = €188 500)
    #    Going forward: created via POST /portfolios/{id}/snapshots
    # ------------------------------------------------------------------
    portfolio_snapshots_table = sa.table(
        'portfolio_snapshots',
        sa.column('id', sa.String),
        sa.column('portfolio_id', sa.String),
        sa.column('value', sa.Numeric),
        sa.column('observed_at', sa.DateTime),
    )
    op.bulk_insert(portfolio_snapshots_table, [
        {
            'id': PORTFOLIO_SNAP_ID,
            'portfolio_id': PORTFOLIO_ID,
            'value': PORTFOLIO_NET_WORTH,
            'observed_at': now,
        }
    ])

    print(f"✅ Seeded demo portfolio '{PORTFOLIO_ID}' with net worth €{PORTFOLIO_NET_WORTH:,}")


def downgrade() -> None:
    """Remove all seeded demo data in reverse FK order."""

    bind = op.get_bind()

    # portfolio_snapshots
    bind.execute(sa.text(f"DELETE FROM portfolio_snapshots WHERE id = '{PORTFOLIO_SNAP_ID}'"))

    # asset_snapshots
    ids_clause = ','.join(f"'{id}'" for id in ALL_SNAPSHOT_IDS)
    bind.execute(sa.text(f"DELETE FROM asset_snapshots WHERE id IN ({ids_clause})"))

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
