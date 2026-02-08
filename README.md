![Strata logo](assets/logo.avif)

# Strata — backend

Strata is a small, domain-driven FastAPI backend for organizing and managing assets (types, portfolios, snapshots, tags). This repository contains the backend application, migrations, tests and docs.

## Quick links
- Source: `backend/`
- Docs: `docs/` (MkDocs)
- Migrations: `backend/alembic/`
- Tests: `tests/unit/`

## Prerequisites
- Python 3.12
- Poetry (recommended for local development)
- Docker & Docker Compose (for containerized runs)

## Quickstart — local (Poetry)
From the repository root:

```bash
cd backend
poetry install
mkdir -p .data
export DATABASE_URL="sqlite://$(pwd)/.data/strata.db"
poetry run alembic -c alembic/alembic.ini upgrade head
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open the API docs at: `http://127.0.0.1:8000/swagger`.

## Docker
Build and run using Docker Compose:

```bash
docker compose up --build
```

The container uses `/app/.data` for the SQLite file. To share the same DB between host and container, mount `./backend/.data:/app/.data` in your compose file or run command.

## Running tests
Run unit tests with Poetry:

```bash
cd backend
poetry run pytest -q
```

## Database & migrations
- Migrations live under `backend/alembic/versions/` and are managed by Alembic.
- The backend will use the `DATABASE_URL` environment variable if set; otherwise it falls back to `backend/.data/strata.db`.

To run migrations locally:

```bash
cd backend
export DATABASE_URL="sqlite://$(pwd)/.data/strata.db"
poetry run alembic -c alembic/alembic.ini upgrade head
```

## Developer notes
- Project follows domain-driven layout: `app/adapters`, `app/application/use_cases`, `app/domain`.
- DB initialization & session management: `app/adapters/outgoing/persistence/database.py`.
- If you want to avoid local README auto-sync, remove or disable the local git hook (see `.git/hooks/`).

## Where to start reading the code
1. `backend/app/main.py` — app entry and router registration
2. `backend/app/adapters/outgoing/persistence` — models, database, repositories
3. `backend/alembic/` — migration scripts
4. `tests/` — unit tests and examples

---

For more detailed developer/docs information see the `docs/` folder.
