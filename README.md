![Strata logo](assets/logo.avif)

[![CI](https://github.com/francoiducat/strata/actions/workflows/main-backend-ci.yml/badge.svg)](https://github.com/francoiducat/strata/actions/workflows/main-backend-ci.yml)
[![codecov](https://codecov.io/gh/francoiducat/strata/graph/badge.svg)](https://codecov.io/gh/francoiducat/strata)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
[![Docs](https://img.shields.io/website?url=https%3A%2F%2Fstrata.ducatillon.net%2Fdocs%2F&label=docs)](https://strata.ducatillon.net/docs/)

# Strata — backend

Strata is a domain-driven FastAPI backend for organizing and managing assets (types, portfolios, snapshots, tags). This repository contains the backend application, migrations, tests and docs.

## Quick links
- Source: `backend/`
- Docs: `docs/` (MkDocs)
- **📚 Live Documentation:** https://strata.ducatillon.net/docs/ (deployed via GitHub Actions)
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

For more detailed developer docs information see the `docs/` folder.

## Quickstart — local (Postgres via Docker Compose)
To run the backend with Postgres using Docker Compose (from repo root):

```bash
docker compose up -d postgres
cd backend
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/strata"
poetry install
poetry run alembic -c alembic/alembic.ini upgrade head
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Ensure the Postgres service is healthy before running migrations. The Docker Compose service name is `postgres` and the default credentials are `postgres/postgres` (for local dev only).
