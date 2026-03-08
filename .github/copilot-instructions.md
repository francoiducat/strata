# Strata — Copilot / AI Agent Instructions

Strata is a universal asset-tracking backend (FastAPI + SQLAlchemy + SQLite) built with hexagonal architecture (Ports & Adapters) and DDD. It tracks portfolios, assets, snapshots, transactions, categories, and tags to compute net worth.

## Build & Test

All commands run from `backend/`:

```bash
# Local dev
poetry install
export DATABASE_URL="sqlite://$(pwd)/.data/strata.db"
poetry run alembic -c alembic/alembic.ini upgrade head
poetry run uvicorn app.main:app --reload --port 8000
# Swagger UI at http://127.0.0.1:8000/swagger

# Docker (from repo root)
docker-compose up --build

# Tests
poetry run pytest -q                                          # full suite
poetry run pytest tests/unit/app/adapters/incoming/ -q       # single directory
poetry run pytest -k "test_create_asset" -q                  # single test by name
poetry run pytest --cov=app --cov-report=term-missing        # with coverage

# New migration (after SQLAlchemy model change)
poetry run alembic revision --autogenerate -m "describe change"
poetry run alembic upgrade head
```

`pytest.ini` sets `testpaths = tests` so run pytest from `backend/`.

## Architecture

The project uses **Hexagonal Architecture** with three strict layers:

```
domain/          ← Pure Python. No FastAPI, SQLAlchemy, or I/O. Entities use Pydantic BaseModel.
application/     ← Use cases orchestrate domain logic. Input via Pydantic command/request DTOs.
adapters/
  incoming/api/  ← Thin FastAPI routes: parse request → call use case → map to response via ApiMapper
  outgoing/      ← SQLAlchemy repository implementations, persistence mappers
```

**Domain layer is kept pure** — no framework imports inside `domain/`. Domain entities inherit `pydantic.BaseModel` with `model_config = ConfigDict(from_attributes=True)`.

**Repository ports** (interfaces) live in `domain/ports/repository/` (e.g. `IAssetRepository`). SQLAlchemy implementations are in `adapters/outgoing/persistence/repository/` and are injected via FastAPI `Depends()` in `adapters/incoming/api/dependencies/`.

**Dependency injection flow**: `dependencies/{domain}.py` wires repositories → use cases → routes use `Depends(use_case_factory)`.

## Key Conventions

**Use case pattern** — each use case is a class with `execute()`:
```python
class CreateAssetUseCase:
    def __init__(self, asset_repo, portfolio_repo, asset_type_repo): ...
    def execute(self, command: CreateAssetRequest) -> Asset: ...
```
Input is a Pydantic `BaseModel` command/request DTO defined in the same use case file.

**Route pattern** — routes are static methods inside a class, returned via `get_router()`:
```python
class AssetRoutes:
    @staticmethod
    def get_router() -> APIRouter: ...
```
Registered in `main.py` with `app.include_router(..., prefix="/api/v1")`.

**Validation is layered**:
1. Shape/types → Pydantic schema (incoming adapter, `schemas/`)
2. Existence checks → use case
3. Business invariants → domain entity
4. Data integrity → DB constraints / repository catches `IntegrityError`

**Mappers** exist at two boundaries:
- `adapters/incoming/api/mappers/api_mapper.py` — domain entity → API response schema
- `adapters/outgoing/persistence/mappers/` — SQLAlchemy model ↔ domain entity

**Exception handling**: Domain exceptions (e.g. `AssetNotFound`) are defined in `domain/exceptions/Exceptions.py` and mapped to HTTP 404 in `main.py` exception handlers. Add new domain exceptions there and register a handler.

**Asset types** are a fixed reference list seeded via Alembic migration. Real codes in the DB: `CHECKING_ACCOUNT`, `SAVINGS_ACCOUNT`, `CASH`, `REAL_ESTATE`, `STOCKS`, `CRYPTO`, `BONDS`, `PERSONAL_PROPERTY`, `VEHICLE`, `LOAN`, `COLLECTIBLES`, `BUSINESS`, `OTHER`.

## Testing Conventions

Tests live in `backend/tests/`. Two suites:

**Unit tests** (`tests/unit/`): zero real DB.
- Route tests use `app.dependency_overrides` to inject fake use cases.
- Use case tests use fake in-memory repositories backed by Python dicts (see `conftest.py` for `dummy_asset_repository`, `dummy_portfolio_repository`).

**Integration tests** (`tests/integration/`): use a dedicated `sqlite:///:memory:` engine, call `Base.metadata.create_all(engine)` at setup, and override `get_db_session` via `app.dependency_overrides`. The production `strata.db` is never touched.

When adding a use case, add a corresponding unit test in `tests/unit/app/` before touching adapters.

## ORM vs Domain Entity Rule

**Write use cases must construct ORM models directly** (never Pydantic domain entities) — `session.add()` requires SQLAlchemy ORM instances. See `CreatePortfolioUseCase` and `TakePortfolioSnapshotUseCase` as reference patterns. Example:

```python
from app.adapters.outgoing.persistence.models.asset import AssetModel
new_asset = AssetModel(id=str(uuid4()), portfolio_id=str(command.portfolio_id), ...)
return self.asset_repository.save(new_asset)
```

## Standard Error Responses

All domain errors return a JSON body with `detail` (string). Domain exceptions (e.g. `AssetNotFound`, `CategoryNotFound`) are defined in `domain/exceptions/Exceptions.py` and mapped to HTTP 404 in `main.py` exception handlers. Add new domain exceptions there and register a handler.

## Current API Endpoints

All routes are under `/api/v1`:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/portfolios/` | List all portfolios |
| POST | `/portfolios/` | Create portfolio |
| GET | `/portfolios/{portfolio_id}` | Get portfolio by ID |
| DELETE | `/portfolios/{portfolio_id}` | Delete portfolio |
| POST | `/portfolios/{portfolio_id}/snapshots` | Take portfolio snapshot |
| GET | `/portfolios/{portfolio_id}/snapshots` | Get portfolio snapshots |
| GET | `/assets/` | List all assets |
| POST | `/assets/` | Create asset |
| GET | `/assets/{asset_id}` | Get asset by ID |
| PUT | `/assets/{asset_id}` | Update asset |
| DELETE | `/assets/{asset_id}` | Delete asset |

## Codebase Map

| Concern | Path |
|---------|------|
| Domain entities | `backend/app/domain/entities/` |
| Repository interfaces | `backend/app/domain/ports/repository/` |
| Use cases | `backend/app/application/use_cases/{asset,portfolio,category,asset_snapshot,asset_type}/` |
| HTTP routes | `backend/app/adapters/incoming/api/routes/` |
| Pydantic schemas | `backend/app/adapters/incoming/api/schemas/` |
| DI providers | `backend/app/adapters/incoming/api/dependencies/` |
| API mapper | `backend/app/adapters/incoming/api/mappers/api_mapper.py` |
| Persistence repos | `backend/app/adapters/outgoing/persistence/repository/` |
| SQLAlchemy models | `backend/app/adapters/outgoing/persistence/models/` |
| DB migrations | `backend/alembic/versions/` |
| Tests | `backend/tests/unit/` (unit) · `backend/tests/integration/` (integration) |
| App entry point | `backend/app/main.py` |

## Config & Secrets

- `DATABASE_URL` env var controls the DB. Defaults to `backend/.data/strata.db`.
- Local overrides via `backend/.env` (loaded by `python-dotenv`). Never commit secrets.
- Docker compose mounts `./backend/.data:/app/.data` for persistent SQLite.

---
For deep-dive docs: `.github/PRD.md` · `docs/` (live at https://strata.ducatillon.net/docs/)