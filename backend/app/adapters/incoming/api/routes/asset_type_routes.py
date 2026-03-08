from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.use_cases.asset_type.get_all_asset_types import GetAllAssetTypesUseCase
from app.application.use_cases.asset_type.get_asset_type import GetAssetTypeUseCase
from app.adapters.incoming.api.dependencies.asset_types import (
    get_all_asset_types_use_case,
    get_asset_type_use_case,
)
from app.adapters.incoming.api.mappers.api_mapper import ApiMapper
from app.adapters.incoming.api.schemas.asset_type_response import AssetTypeResponse
from app.adapters.incoming.api.schemas.error_response import ErrorResponse


class AssetTypeRoutes:

    @staticmethod
    def get_router() -> APIRouter:
        router = APIRouter(prefix="/asset-types", tags=["Asset Types"])

        @router.get("/", response_model=List[AssetTypeResponse])
        def get_all_asset_types(
            use_case: GetAllAssetTypesUseCase = Depends(get_all_asset_types_use_case),
        ):
            asset_types = use_case.execute()
            return ApiMapper.to_asset_type_response_list(asset_types)

        @router.get(
            "/{asset_type_id}",
            response_model=AssetTypeResponse,
            responses={404: {"model": ErrorResponse}},
        )
        def get_asset_type(
            asset_type_id: UUID,
            use_case: GetAssetTypeUseCase = Depends(get_asset_type_use_case),
        ):
            asset_type = use_case.execute(asset_type_id)
            return ApiMapper.to_asset_type_response(asset_type)

        return router
