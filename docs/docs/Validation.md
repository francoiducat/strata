# Validation Strategy in Hexagonal Architecture

In a Hexagonal (Ports & Adapters) Architecture, validation is a layered responsibility. Each layer has a distinct role in ensuring data is correct, consistent, and compliant with business rules. This prevents invalid data from corrupting the application's state.

For setup instructions, see the [Quick Start](QuickStart.md) guide.

## Core Philosophy

The guiding principle is to validate as early as possible and as close to the source of the data as is appropriate for the type of validation being performed.

- **Business Invariants** belong in the **Domain Layer**.
- **Input Shape & Type** belongs in the **Incoming Adapter**.
- **Data Integrity** belongs in the **Outgoing Adapter / Database**.
- **Orchestration & Flow** belongs in the **Application Layer**.

---

## The Validation Chain

Here is the journey of validation for a typical request.

### 1. Incoming Adapter: API Schemas (Pydantic)

- **Responsibility**: To validate the shape, data types, and presence of required fields in an incoming HTTP request payload.
- **Location**: `backend/app/adapters/incoming/api/schemas/`
- **Example**: When a user sends a `POST` request to create an asset, a Pydantic schema immediately checks if `name` is a string, `value` is a float, and `asset_type_id` is a valid UUID. If validation fails, FastAPI automatically returns a `422 Unprocessable Entity` response.

```python
# In a Pydantic schema
class AssetCreateSchema(BaseModel):
    name: str = Field(..., min_length=3)
    value: float
    asset_type_id: UUID
```

### 2. Application Layer: Use Cases

- **Responsibility**: To handle application-specific validation and orchestrate business logic. This includes checking for the existence of entities before acting on them.
- **Location**: `backend/app/application/use_cases/`
- **Example**: The `GetAssetUseCase` receives an `asset_id`. Before returning the asset, it validates that an asset with that ID actually exists. If not, it raises a domain-specific `AssetNotFound` exception. This makes the use case's contract clear: it either returns a valid `Asset` or it fails explicitly.

```python
# In GetAssetUseCase.execute()
asset = self.asset_repository.find_by_id(asset_id)
if asset is None:
    raise AssetNotFound(f"Asset with id {asset_id} not found.")
return asset
```

### 3. Domain Layer: Entities (Business Models)

- **Responsibility**: To enforce core business rules and invariants. A domain entity should be self-validating and guarantee it is always in a consistent state.
- **Location**: `backend/app/domain/entities/`
- **Example**: An `Asset` entity might have a business rule that its `value` can never be negative. This logic is placed directly within the entity itself, often in `__post_init__` for dataclasses.

```python
# In domain/entities/asset.py
from dataclasses import dataclass, field

@dataclass
class Asset:
    id: UUID
    name: str
    value: float

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Asset value cannot be negative.")
        if not self.name:
            raise ValueError("Asset name cannot be empty.")
```

### 4. Outgoing Adapter: Repository & Database

- **Responsibility**: To enforce final data integrity constraints at the persistence level.
- **Location**: `backend/app/adapters/outgoing/database/models/` (ORM Models) and the database schema itself.
- **Example**: The `assets` table in the database has a `UNIQUE` constraint on the `name` column. If the repository implementation tries to save an `AssetModel` with a name that already exists, the database will reject the transaction, and SQLAlchemy will raise an `IntegrityError`. The repository implementation can catch this specific error and re-raise it as a more specific domain exception, like `AssetNameNotUnique`.

---

## Handling Failures

Each layer handles validation failures appropriately:

- **API Adapter**: Catches domain exceptions (like `AssetNotFound`) from the use case and translates them into appropriate HTTP status codes (like `404 Not Found`).
- **Use Case**: Catches specific repository/database exceptions (like `AssetNameNotUnique`) and can decide whether to handle them or let them propagate to the API layer.
- **Domain Entity**: Raises exceptions (`ValueError`, `TypeError`, or custom domain exceptions) if a business rule is violated.
- **Repository**: Catches low-level database exceptions (`IntegrityError`) and translates them into domain-specific exceptions.

This layered approach ensures that your core business logic is pure, protected, and completely independent of the delivery mechanism (API) and persistence technology (database).