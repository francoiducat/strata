# 🏗️ Hexagonal Architecture with FastAPI

This document outlines the architecture of the Strata backend, built with FastAPI and following Hexagonal Architecture (Ports & Adapters). This design ensures modularity, testability, and maintainability.

## Core Principles

1. **Separation of Concerns**: Distinct layers with clear responsibilities.
2. **Dependency Inversion**: The core logic (the "hexagon") is independent of frameworks and external tech. It defines "ports" (interfaces), and adapters implement these ports.
3. **Testability**: Business rules are decoupled from infrastructure, making them easy to test.

## Back End Directory Structure

```bash
backend/
├── Dockerfile
├── alembic                    # Alembic folder
│ ├── README
│ ├── env.py
│ ├── script.py.mako  
│ └── versions                 # Alembic migration scripts
├── alembic.ini
├── app                        # Main application folder
│ ├── adapters                                                    
│ │ ├── incoming               # Primary interactions: FastAPI app, routers, schemas, and mappers
│ │ └── outgoing               # Persistence layer, Entity Models, Mappers, SQLAlchemy repository implementations.
│ ├── application              # Orchestration layer (use cases), depends on domain ports
│ │ └── use_cases
│ ├── domain                   # The core business logic (the "hexagon")
│ │ ├── entities               # Business entities
│ │ ├── exceptions
│ │ └── ports                  # Interfaces for repositories (IAssetRepository.py) and services 
│ └── main.py
├── poetry.lock
├── pyproject.toml
└── scripts                    # Utility scripts
```

## Application Entrypoint & Configuration

- **main.py:** (`backend/app/main.py`).
- **alembic/versions:** Alembic migrations for DB schema.