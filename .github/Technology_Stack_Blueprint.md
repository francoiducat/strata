# Technology Stack Blueprint — Strata (backend)

Generated: 2026-02-08

## Summary
- Project: Strata — backend
- Primary language: Python 3.12
- Framework: FastAPI
- Database: SQLite (via SQLAlchemy + Alembic migrations)
- Packaging & environment: Poetry
- Web server: Uvicorn
- Testing: pytest

---

## 1. Technology Identification
- Languages detected: Python (.py)
- Key files scanned:
  - `pyproject.toml` — declares dependencies and scripts
  - `app/main.py` — FastAPI application entrypoint
  - `app/adapters/outgoing/persistence/database.py` — DB config
  - `alembic/env.py`, `alembic/versions/` — migrations
  - `Dockerfile` — container image config
  - `tests/` — pytest test suite

### Dependency versions (from `pyproject.toml`)
- python: >=3.12,<3.13
- fastapi: >=0.128.0,<0.129.0
- starlette: >=0.50.0,<0.51.0
- uvicorn: >=0.40.0,<0.41.0
- sqlalchemy: >=2.0.45,<3.0.0
- alembic: >=1.18.0,<2.0.0
- pydantic: >=2.12.5,<3.0.0
- pytest: ^8.4 (dev)
- Others: anyio, uvloop, etc.

License: Project license set to GPL-3.0 in `pyproject.toml`.

---

## 2. Core Technologies Analysis — Python / FastAPI

- Python 3.12 is required.
- FastAPI is used for HTTP API with Uvicorn as the ASGI server.
- Application entry is `app/main.py` which constructs `FastAPI(...)` and exposes `/swagger` docs and `/api/v1` routers.
- Error handling: Domain-specific exceptions are mapped to 404s and generic exceptions return 500 with logging.
- Lifespan: an asynccontextmanager is used to manage startup/shutdown and to dispose of the SQLAlchemy engine on shutdown.

Database & Migrations
- SQLAlchemy 2.x is used with DeclarativeBase and `sessionmaker`.
- Database URL behavior:
  - Default: repository-local `backend/.data/strata.db` (constructed in `database.py`).
  - If `DATABASE_URL` is set (e.g., from Docker env or runtime), it will use that.
  - The system tries to create parent directories and falls back to repo-local path if parent's creation fails.
- Alembic is configured under `backend/alembic/alembic.ini` and the migration scripts live in `backend/alembic/versions/`.

Configuration
- Uses `.env` support: `python-dotenv` is loaded from `backend/.env` for non-production runs if `DATABASE_URL` is not already set.

Testing & CI
- Tests exist under `tests/unit/...` and are run with `pytest` (8 tests currently passing locally).
- Coverage artifacts are present under `tests/coverage/`.

Docker
- `backend/Dockerfile` builds with Poetry, sets `WORKDIR /app` and copies `alembic` and `alembic.ini` into the image. It creates `/app/.data`.

---

## 3. Implementation Patterns & Conventions (detected)

### Naming & Structure
- Package structure follows domain-driven design with folders: `app/adapters`, `app/application/use_cases`, `app/domain/entities`, etc.
- Routers are provided via classes such as `AssetRoutes` and `PortfolioRoutes`, then included into the main app via `app.include_router(..., prefix="/api/v1")`.

### Error handling
- Domain-level exceptions are defined in `app/domain/exceptions` and mapped to HTTP status codes in `app/main.py`.
- A middleware logs unhandled exceptions.

### Database access patterns
- Repository pattern: adapters/outgoing/persistence likely contains repository implementations and SQLAlchemy models; models are imported into Alembic env for autogenerate.
- FastAPI dependency `get_db()` yields sessions via `SessionLocal()` and ensures closures in finally.

### Configuration
- Dotenv for local configs; environment variables for container/production.

---

## 4. Usage Examples (extracted)

### Running locally with Poetry
```bash
cd backend
poetry install
# Run migrations using local DB
export DATABASE_URL="sqlite://$(pwd)/.data/strata.db"
mkdir -p .data
poetry run alembic -c alembic/alembic.ini upgrade head
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Running in Docker
- `docker-compose up --build` (ensure `./backend/.data` is mounted to `/app/.data` in the compose file) so container uses the same DB file.

---

## 5. Technology Map (concise)
- FastAPI app -> SQLAlchemy -> SQLite
- Alembic manages migrations against SQLAlchemy models
- Poetry handles virtual env and packaging
- Uvicorn runs the app (ASGI)

---

## 6. Recommendations & Next Steps
1. Prefer environment-driven alembic config: remove hard-coded `alembic.ini` sqlalchemy.url and rely on `DATABASE_URL` and `backend/.env` for local runs.
2. Consider converting to in-project virtualenvs for deterministic dev setup: `poetry config virtualenvs.in-project true`.
3. For production consider a more robust DB than SQLite (Postgres). Keep current patterns so switching is straightforward.
4. Add a `backend/README.md` with the local dev commands and `DATABASE_URL` notes.

---

## Artifacts
- Saved to: `backend/docs/Technology_Stack_Blueprint.md`


*End of generated blueprint.*

