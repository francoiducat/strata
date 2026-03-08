---
title: Strata — Product Requirements Document
version: 0.1
last_updated: 2026-03-06
status: active
doc_type: prd
audience: ai-agent, engineering
---

# Strata — PRD

## 1. Purpose

Single source of truth for AI agents and contributors. For deep-dive documentation, follow the links in section 9.

---

## 2. Problem Statement

Most personal finance / inventory apps are domain-specific: they track investments OR collections OR household inventory. Users who own diverse assets — financial, physical, collectibles, personal property, liabilities — have no single tool to see their complete net worth and organise everything with flexible taxonomy.

---

## 3. Product Summary

**Strata** is a universal asset tracking backend. It lets you catalogue *anything you own or owe*, attach values over time, organise with hierarchical categories and flat tags, and compute net worth across all asset types.

> "Your wealth isn't just money — it's everything you value."

---

## 4. Target Personas

| Persona | Core need |
|---------|-----------|
| **Investor** | Track stocks, crypto, real estate, cash accounts; see total net worth in one view |
| **Collector** | Catalogue LEGO, books, art, vintage items with acquisition cost and current value |
| **Homeowner** | Manage household inventory (furniture, electronics, heirlooms) with valuations |
| **Fashion enthusiast** | Organise wardrobe by type/season/occasion, track purchase price vs. current value |
| **Anyone** | Know what they own and what it is worth |

---

## 5. Core Domain Concepts

### 5.1 Asset Types (accounting classification, 1 per asset)

Fixed reference list (seeded via Alembic migration):

`CHECKING_ACCOUNTS` · `SAVINGS_ACCOUNTS` · `CASH` · `REAL_ESTATE` · `LOAN` · `STOCKS_AND_FUNDS` · `CRYPTO` · `PERSONAL_ITEMS` · `COLLECTIONS` · `OTHER`

Users may also create custom types.

### 5.2 Categories (WordPress-style, many-to-many)

- Hierarchical: `Real Estate > Residential > Apartments`
- Cross-cutting: `Income Generating Assets`, `Primary Residence`
- An asset can belong to **multiple** categories simultaneously.

### 5.3 Tags (flat labels, many-to-many)

Additional metadata for filtering: `paris`, `vintage`, `unopened`.

### 5.4 Transactions

| Type | Meaning |
|------|---------|
| `ACQUIRE` | Buying / receiving (increases quantity) |
| `DISPOSE` | Selling / giving away (decreases quantity) |
| `ADJUST` | Manual correction |

Liabilities use negative `unit_price` on `ACQUIRE` (e.g., taking a loan).

### 5.5 Snapshots

- **AssetSnapshot**: manually entered value at a point in time.
- **PortfolioSnapshot**: auto-calculated total across all assets at a point in time.
- Portfolio valuation uses the **latest** snapshot per asset.

### 5.6 Net Worth formula

```
Net Worth = Σ (latest AssetSnapshot.value for each asset)
```

Positive assets increase it; liabilities (LOAN, MORTGAGE) have negative values and decrease it.

---

## 6. Functional Requirements

### Must Have

- [ ] CRUD for **Portfolio** (name, base_currency)
- [ ] CRUD for **Asset** (linked to a portfolio and asset type)
- [ ] CRUD for **AssetSnapshot** (value + observed_at per asset)
- [ ] CRUD for **Transaction** (ACQUIRE / DISPOSE / ADJUST)
- [ ] CRUD for **Category** with hierarchical parent/child support
- [ ] CRUD for **Tag** and asset↔tag association
- [ ] Read-only **AssetType** reference data (seeded)
- [ ] Portfolio total value computation (latest snapshot per asset)

### Should Have

- [ ] Filter assets by category, tag, asset type, disposed flag
- [ ] Portfolio snapshot recording and history
- [ ] Asset disposal workflow (set `disposed = true`)

### Out of Scope (current version)

- Real-time market price feeds
- Multi-user / authentication
- Frontend / mobile clients

---

## 7. Technical Constraints

| Area | Decision |
|------|----------|
| **Language** | Python 3.12 |
| **Framework** | FastAPI + Pydantic (validation) |
| **ORM** | SQLAlchemy |
| **Migrations** | Alembic |
| **Database** | SQLite (default); PostgreSQL-ready |
| **Dependency mgmt** | Poetry |
| **Architecture** | Hexagonal (Ports & Adapters) + DDD |
| **Server** | Uvicorn (ASGI) |
| **Container** | Docker / Docker Compose |

---

## 8. Architecture Rules (for agents modifying code)

1. **Domain layer is pure** — no FastAPI, SQLAlchemy, or I/O imports inside `domain/`.
2. **Use cases orchestrate** — business logic lives in `application/use_cases/`, not in routes.
3. **Adapters are thin** — routes parse request → call use case → map result to response.
4. **Validation is layered**:
   - Shape / types → Pydantic schema (incoming adapter)
   - Existence checks → use case
   - Business invariants → domain entity (`__post_init__`)
   - Data integrity → DB constraints / repository catches `IntegrityError`
5. **Schema changes** require an Alembic migration in `alembic/versions/`.
6. **Never hardcode secrets** — use environment variables / `.env`.

---

## 9. Codebase Map

| Concern | Path |
|---------|------|
| Domain entities | `backend/app/domain/entities/` |
| Repository interfaces (ports) | `backend/app/domain/ports/repository/` |
| Use cases | `backend/app/application/use_cases/{asset,portfolio,category,asset_snapshot,asset_type}/` |
| HTTP routes | `backend/app/adapters/incoming/api/routes/` |
| Pydantic schemas | `backend/app/adapters/incoming/api/schemas/` |
| Persistence (SQLAlchemy) | `backend/app/adapters/outgoing/persistence/` |
| DB migrations | `backend/alembic/versions/` |
| Tests | `backend/tests/unit/` |
| App entry point | `backend/app/main.py` |
| CLI helpers | `backend/app/cli.py` |

**Entities:** `Portfolio` · `Asset` · `AssetType` · `AssetSnapshot` · `PortfolioSnapshot` · `Transaction` · `Category` · `Tag`

**Repository ports:** `IAssetRepository` · `IPortfolioRepository` · `ICategoryRepository` · `IAssetSnapshotRepository` · `IPortfolioSnapshotRepository` · `IAssetTypeRepository` · `ITagRepository` · `ITransactionRepository`

---

## 10. API Surface (current)

Base URL: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/swagger`

| Domain | Route file |
|--------|-----------|
| Assets | `adapters/incoming/api/routes/asset_routes.py` |
| Portfolios | `adapters/incoming/api/routes/portfolio_routes.py` |

---

## 11. Data Model Quick Reference

See [DataModel.md](../docs/docs/DataModel.md) for ER and class diagrams.

Key relationships:
- `Portfolio` 1→N `Asset`
- `Asset` N→1 `AssetType`
- `Asset` N→N `Category` (via `ASSET_CATEGORY`)
- `Asset` N→N `Tag` (via `ASSET_TAG`)
- `Asset` 1→N `Transaction`
- `Asset` 1→N `AssetSnapshot`
- `Portfolio` 1→N `PortfolioSnapshot`

---

## 12. Dev Commands

```bash
# Run with Docker (recommended)
docker-compose up

# Run locally
cd backend
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload --port 8000

# Tests
poetry run pytest -q
poetry run pytest --cov=app --cov-report=term-missing

# New migration (after model change)
poetry run alembic revision --autogenerate -m "describe change"
poetry run alembic upgrade head
```

---

## 13. Acceptance Criteria (agent checklist)

When implementing or modifying a feature, verify:

- [ ] Domain entity stays pure (no framework imports)
- [ ] Use case has a corresponding unit test in `tests/unit/`
- [ ] Route is thin (parse → use case → response)
- [ ] Pydantic schema validates input shape at the adapter boundary
- [ ] Any DB schema change has an Alembic migration
- [ ] `poetry run pytest -q` passes with no regressions
- [ ] No secrets committed

---

## 14. Reference Documentation

| Doc | Content |
|-----|---------|
| [StrataApp.md](../docs/docs/StrataApp.md) | Product overview, personas, philosophy |
| [Features.md](../docs/docs/Features.md) | Feature list |
| [MentalModel.md](../docs/docs/MentalModel.md) | Asset Type / Category / Tag mental model |
| [DataModel.md](../docs/docs/DataModel.md) | ER diagram + class diagram |
| [Architecture.md](../docs/docs/Architecture.md) | Hexagonal architecture, directory structure |
| [Validation.md](../docs/docs/Validation.md) | Layered validation strategy with examples |
| [UseCases.md](../docs/docs/UseCases.md) | Concrete examples (bank account, wardrobe, real estate…) |
| [Alembic.md](../docs/docs/Alembic.md) | Migration workflow |
| [TechStack.md](../docs/docs/TechStack.md) | Full tech stack list |
| [QuickStart.md](../docs/docs/QuickStart.md) | Setup and run instructions |
