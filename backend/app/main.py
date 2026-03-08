from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
import logging
from fastapi.responses import JSONResponse

from app.adapters.incoming.api.routes.asset_routes import AssetRoutes
from app.adapters.incoming.api.routes.portfolio_routes import PortfolioRoutes
from app.adapters.incoming.api.routes.asset_type_routes import AssetTypeRoutes
from app.adapters.incoming.api.routes.category_routes import CategoryRoutes
from app.adapters.incoming.api.routes.tag_routes import TagRoutes
from app.adapters.incoming.api.schemas.error_response import ErrorResponse
from app.adapters.outgoing.persistence.database import engine
from app.domain.exceptions import (
    AssetNotFound,
    PortfolioNotFound,
    AssetTypeNotFound,
    CategoryNotFound,
    TagNotFound,
    DuplicateName,
    CategoryHasChildren,
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
DOMAIN_NOT_FOUND_EXCEPTIONS = (
    AssetNotFound, PortfolioNotFound, AssetTypeNotFound, CategoryNotFound,
    TagNotFound, DuplicateName, CategoryHasChildren,
)


@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        # If it's a domain NotFound exception, re-raise so the specific handler below handles it
        if isinstance(exc, DOMAIN_NOT_FOUND_EXCEPTIONS):
            raise
        logging.exception("Unhandled error:")
        err = ErrorResponse(code="INTERNAL_ERROR", message="An unexpected error occurred.", status=500)
        return JSONResponse(status_code=500, content=err.model_dump())


# Domain-specific exception handlers (map domain errors to HTTP responses)
@app.exception_handler(AssetNotFound)
async def handle_asset_not_found(request: Request, exc: AssetNotFound):
    err = ErrorResponse(code="ASSET_NOT_FOUND", message=str(exc), status=404)
    return JSONResponse(status_code=404, content=err.model_dump())


@app.exception_handler(PortfolioNotFound)
async def handle_portfolio_not_found(request: Request, exc: PortfolioNotFound):
    err = ErrorResponse(code="PORTFOLIO_NOT_FOUND", message=str(exc), status=404)
    return JSONResponse(status_code=404, content=err.model_dump())


@app.exception_handler(AssetTypeNotFound)
async def handle_asset_type_not_found(request: Request, exc: AssetTypeNotFound):
    err = ErrorResponse(code="ASSET_TYPE_NOT_FOUND", message=str(exc), status=404)
    return JSONResponse(status_code=404, content=err.model_dump())


@app.exception_handler(CategoryNotFound)
async def handle_category_not_found(request: Request, exc: CategoryNotFound):
    err = ErrorResponse(code="CATEGORY_NOT_FOUND", message=str(exc), status=404)
    return JSONResponse(status_code=404, content=err.model_dump())


@app.exception_handler(TagNotFound)
async def handle_tag_not_found(request: Request, exc: TagNotFound):
    err = ErrorResponse(code="TAG_NOT_FOUND", message=str(exc), status=404)
    return JSONResponse(status_code=404, content=err.model_dump())


@app.exception_handler(DuplicateName)
async def handle_duplicate_name(request: Request, exc: DuplicateName):
    err = ErrorResponse(code="DUPLICATE_NAME", message=str(exc), status=409)
    return JSONResponse(status_code=409, content=err.model_dump())


@app.exception_handler(CategoryHasChildren)
async def handle_category_has_children(request: Request, exc: CategoryHasChildren):
    err = ErrorResponse(code="CATEGORY_HAS_CHILDREN", message=str(exc), status=409)
    return JSONResponse(status_code=409, content=err.model_dump())


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Asset Tree API"}

app.include_router(AssetRoutes.get_router(), prefix="/api/v1")
app.include_router(PortfolioRoutes.get_router(), prefix="/api/v1")
app.include_router(AssetTypeRoutes.get_router(), prefix="/api/v1")
app.include_router(CategoryRoutes.get_router(), prefix="/api/v1")
app.include_router(TagRoutes.get_router(), prefix="/api/v1")
