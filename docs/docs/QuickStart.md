# 🚀 Quick Start Guide

Welcome to the Strata Developer Docs!

This guide helps you set up and run the backend, and gives you a fast overview of the core concepts.

## Run Strata App 

### Prerequisites

- Docker & Docker Compose (recommended)
- OR Python 3.12+ with Poetry

#### Run with Docker (Option 1: Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd strata

# Start the application with Docker Compose
docker-compose up

# Backend API: http://localhost:8000
# MkDocs Documentation: http://localhost:8001
```

The backend will automatically run database migrations on startup.

#### Run with Poetry (Option 2)

```bash
# Clone the repository
git clone <repository-url>
cd strata/backend

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run persistence migrations
poetry run alembic upgrade head

# Start the FastAPI server
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Access Points

- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/swagger
- **MkDocs Documentation:** http://localhost:8001 (if running with Docker)

## Database & Migrations

### SQLite 

![image](https://sqlite.org/images/sqlite370_banner.svg){ width="75" loading=lazy}

Strat App currently uses an SQLite database

### Alembic

Strat App uses [Alembic](Alembic.md) for database migrations.

### Quick checks

Verify resolved DB path:

```bash
docker-compose exec -T backend python -c "import os; print(os.path.join(os.getcwd(), '.data', 'strata.db'))"
```

Inspect tables:

```bash
docker-compose exec -T backend sqlite3 /app/.data/strata.db ".tables"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
