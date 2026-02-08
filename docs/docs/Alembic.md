# Alembic Migrations

## Why Alembic ?

Alembic is a **database migration tool** for SQLAlchemy. Main reasons to use Alembic are:

|         | Explanation                                                            | Promise                                                         |
| ------------- |------------------------------------------------------------------------|-----------------------------------------------------------------|
| **Versioning**    | Database schema management over time.                                  | Every schema change is tracked and reversible.                  |
| **Consistency**   | Same migration workflow across environments.                           | Dev, qualif, prod databases stay in sync with SQLAlchemy models. |
| **Safety**        | Structured way to evolve the database schema as the application grows. | No more accidental schema drift or manual database changes.     |
| **Collaboration** | Improved collaboaration.                                               | Multiple developers can work on the same database schema without conflicts.                                                                |

## How to Use Alembic ?

### 1. Initialisation (First-Time Setup)

Set up the migration environment:

1.1 Go to the directory where you want your alembic migration folder:

```bash
   cd /where/alembic/ini/is/located
```

1.2 Run the Alembic init command:

```bash
   alembic init migrations
```

This will create a folder with all necessary template files:

- `env.py`: Configuration for Alembic's migration.
- `script.py.mako`: Template for generating migration scripts.
- `versions/`: Directory where migration scripts are stored.


### 2. Bringing Your Schema Under Alembic Control

If you are starting from scratch or have an existing database with no Alembic migrations, you must create an **initial migration**. This migration will represent the current state of your models and database.

#### 2.1 Make Sure Your Models Are Up to Date

- Ensure all your SQLAlchemy models reflect the tables and columns you want in your database.

#### 2.2 Create the Initial Migration

Run this command from your project root:

```bash
alembic revision --autogenerate -m "Initial migration"
```

This will generate a migration script in `versions/`.

**Review the script** to ensure it matches your intended schema.

#### 2.3 Apply the Migration

Apply the migration to your database:

```bash
alembic upgrade head
```

### 3. Typical Alembic Workflow

3.1 **Edit your SQLAlchemy models**.

3.2 **Create initiatial migration:**

```bash
   alembic revision --autogenerate -m "Initial migration"
```

💡This command auto-generates the migration file by comparing your SQLAlchemy models to the current state of the database.

3.3 **Adding a Second Migration** (add, remove, or modify tables/columns)

**Option A**: Generate a migration automatically on SQLAlchemy **Model Changes**

If you make further changes to your SQLAlchemy models (e.g., adding a new column).

- Generate the migration:

```bash
alembic revision --autogenerate -m "Add new column to asset table"
```

Alembic will detect the changes and populate the `upgrade()` and `downgrade()` methods with the necessary SQLAlchemy operations.

!!! abstract "2ec8169a394e_initial_schema_with_all_tables.py"
    Review the generated migration file to ensure it correctly captures your intended changes.


**Option B**: Create manual migration.

For custom operations like **data seeding**, complex transformations etc. 

- Create an empty migration skeleton

```bash
alembic revision -m "Seed asset types reference data"
```
!!! abstract "7de8469a594f_seed_asset_types_reference_data.py"
    Review the created migration file with empty `upgrade()` and `downgrade()` methods.
    Manually edit these functions to include your logic.

Example: seeding `asset_types` reference data:

```python
def upgrade():
    # Example: Insert reference data into the asset_types table
    op.bulk_insert(
        asset_types_table,
        [
            {"id": 1, "name": "CHECKING_ACCOUNTS"},
            {"id": 2, "name": "SAVINGS_ACCOUNTS"},
            {"id": 3, "name": "REAL_ESTATE"},
        ],
    )

def downgrade():
    # Example: Remove the seeded data
    op.execute("DELETE FROM asset_types WHERE id IN (1, 2, 3)")
```

3.4 **Apply the migration:**

```bash
alembic upgrade head
```

## Useful Alembic Commands

- **Check current migration state:**

```bash
  alembic current
```

- **Rollback last migration:**

```bash
  alembic downgrade -1
```

- **Stamp the database (mark as up-to-date without running migrations):**

```bash
  alembic stamp head
```

- **Show migration history:**

```bash
  alembic history
```

- **Usage with poetry**:

```bash
  poetry run alembic revision --autogenerate -m "Migration message"
  poetry run alembic upgrade head
```
