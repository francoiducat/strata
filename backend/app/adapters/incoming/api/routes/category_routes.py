from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.application.use_cases.category.create_category import CreateCategoryCommand, CreateCategoryUseCase
from app.application.use_cases.category.get_all_categories import GetAllCategoriesUseCase
from app.application.use_cases.category.get_category import GetCategoryUseCase
from app.application.use_cases.category.delete_category import DeleteCategoryUseCase
from app.application.use_cases.category.add_asset_to_category import (
    AddAssetToCategoryCommand,
    AddAssetToCategoryUseCase,
)
from app.adapters.incoming.api.dependencies.categories import (
    create_category_use_case,
    get_all_categories_use_case,
    get_category_use_case,
    delete_category_use_case,
    add_asset_to_category_use_case,
)
from app.adapters.incoming.api.mappers.api_mapper import ApiMapper
from app.adapters.incoming.api.schemas.category_request import CategoryCreateRequest, CategoryAssetAssignRequest
from app.adapters.incoming.api.schemas.category_response import CategoryResponse
from app.adapters.incoming.api.schemas.error_response import ErrorResponse


class CategoryRoutes:

    @staticmethod
    def get_router() -> APIRouter:
        router = APIRouter(prefix="/categories", tags=["Categories"])

        @router.get("/", response_model=List[CategoryResponse])
        def get_all_categories(
            use_case: GetAllCategoriesUseCase = Depends(get_all_categories_use_case),
        ):
            categories = use_case.execute()
            return ApiMapper.to_category_response_list(categories)

        @router.post(
            "/",
            response_model=CategoryResponse,
            status_code=status.HTTP_201_CREATED,
            responses={409: {"model": ErrorResponse}},
        )
        def create_category(
            request: CategoryCreateRequest,
            use_case: CreateCategoryUseCase = Depends(create_category_use_case),
        ):
            command = CreateCategoryCommand(name=request.name, parent_id=request.parent_id)
            category = use_case.execute(command)
            return ApiMapper.to_category_response(category)

        @router.get(
            "/{category_id}",
            response_model=CategoryResponse,
            responses={404: {"model": ErrorResponse}},
        )
        def get_category(
            category_id: UUID,
            use_case: GetCategoryUseCase = Depends(get_category_use_case),
        ):
            category = use_case.execute(category_id)
            return ApiMapper.to_category_response(category)

        @router.delete(
            "/{category_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
        )
        def delete_category(
            category_id: UUID,
            use_case: DeleteCategoryUseCase = Depends(delete_category_use_case),
        ):
            use_case.execute(category_id)
            return None

        @router.get(
            "/{category_id}/children",
            response_model=List[CategoryResponse],
            responses={404: {"model": ErrorResponse}},
        )
        def get_category_children(
            category_id: UUID,
            get_cat_use_case: GetCategoryUseCase = Depends(get_category_use_case),
        ):
            # Verify category exists first
            category = get_cat_use_case.execute(category_id)
            children = category.children if hasattr(category, "children") and category.children else []
            return ApiMapper.to_category_response_list(children)

        @router.post(
            "/{category_id}/assets",
            response_model=CategoryResponse,
            responses={404: {"model": ErrorResponse}},
        )
        def assign_asset_to_category(
            category_id: UUID,
            request: CategoryAssetAssignRequest,
            use_case: AddAssetToCategoryUseCase = Depends(add_asset_to_category_use_case),
            get_cat_use_case: GetCategoryUseCase = Depends(get_category_use_case),
        ):
            command = AddAssetToCategoryCommand(asset_id=request.asset_id, category_id=category_id)
            use_case.execute(command)
            category = get_cat_use_case.execute(category_id)
            return ApiMapper.to_category_response(category)

        return router
