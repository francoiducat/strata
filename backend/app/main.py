from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
import logging
from fastapi.responses import JSONResponse

from app.adapters.incoming.api.routes.asset_routes import AssetRoutes
from app.adapters.incoming.api.routes.portfolio_routes import PortfolioRoutes
from app.adapters.outgoing.persistence.database import engine
from app.domain.exceptions import (
    AssetNotFound,
    PortfolioNotFound,
    AssetTypeNotFound,
    CategoryNotFound,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- startup ----
    print("🚀 Application starting")
    yield

    # ---- shutdown ----
    print("🛑 Application shutting down")
    engine.dispose()
app = FastAPI(
    title="Assets API",
    description="API for managing assets.",
    version="1.0.0",
    docs_url="/swagger",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan)

# Domain exceptions tuple for easy checking
DOMAIN_NOT_FOUND_EXCEPTIONS = (AssetNotFound, PortfolioNotFound, AssetTypeNotFound, CategoryNotFound)


@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        # If it's a domain NotFound exception, re-raise so the specific handler below handles it
        if isinstance(exc, DOMAIN_NOT_FOUND_EXCEPTIONS):
            raise
        logging.exception("Unhandled error:")
        return JSONResponse(status_code=500, content={"detail": str(exc)})


# Domain-specific exception handlers (map domain errors to HTTP responses)
@app.exception_handler(AssetNotFound)
async def handle_asset_not_found(request: Request, exc: AssetNotFound):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(PortfolioNotFound)
async def handle_portfolio_not_found(request: Request, exc: PortfolioNotFound):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(AssetTypeNotFound)
async def handle_asset_type_not_found(request: Request, exc: AssetTypeNotFound):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(CategoryNotFound)
async def handle_category_not_found(request: Request, exc: CategoryNotFound):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Asset Tree API"}

app.include_router(AssetRoutes.get_router(), prefix="/api/v1")
app.include_router(PortfolioRoutes.get_router(), prefix="/api/v1")
