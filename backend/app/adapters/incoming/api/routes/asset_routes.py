from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from app.application.use_cases.asset.create_asset import (
    CreateAssetRequest,
    CreateAssetUseCase,
)
from app.application.use_cases.asset.get_all_assets import GetAllAssetsUseCase
from app.application.use_cases.asset.get_asset import GetAssetUseCase
from app.application.use_cases.asset.update_asset import UpdateAssetCommand, UpdateAssetUseCase
from app.application.use_cases.asset.delete_asset import DeleteAssetUseCase
from app.adapters.incoming.api.dependencies.assets import (
    create_asset_use_case,
    get_all_assets_use_case,
    get_asset_use_case,
    update_asset_use_case,
    delete_asset_use_case,
)
from app.adapters.incoming.api.mappers.api_mapper import ApiMapper
from app.adapters.incoming.api.schemas.asset_request import AssetCreateRequest, AssetUpdateRequest
from app.adapters.incoming.api.schemas.asset_response import AssetResponse

class AssetRoutes:

    @staticmethod
    def get_router() -> APIRouter:
        router = APIRouter(prefix="/assets", tags=["Assets"])

        @router.get("/", response_model=List[AssetResponse])
        def get_all_assets(
            get_all_use_case: GetAllAssetsUseCase = Depends(get_all_assets_use_case),
        ):
            assets = get_all_use_case.execute()
            return ApiMapper.to_asset_response_list(assets)

        @router.get("/{asset_id}", response_model=AssetResponse)
        def get_asset_by_id(
            asset_id: UUID, use_case: GetAssetUseCase = Depends(get_asset_use_case)
        ):
            asset = use_case.execute(asset_id)
            return ApiMapper.to_asset_response(asset)

        @router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
        def create_asset(
            request: AssetCreateRequest,
            create_use_case: CreateAssetUseCase = Depends(create_asset_use_case),
        ):
            asset_request = CreateAssetRequest(**request.model_dump())
            new_asset = create_use_case.execute(asset_request)
            return ApiMapper.to_asset_response(new_asset)

        @router.put("/{asset_id}", response_model=AssetResponse)
        def update_asset(
            asset_id: UUID,
            request: AssetUpdateRequest,
            use_case: UpdateAssetUseCase = Depends(update_asset_use_case),
        ):
            """Update an existing asset's attributes."""
            command = UpdateAssetCommand(asset_id=asset_id, **request.model_dump())
            updated_asset = use_case.execute(command)
            return ApiMapper.to_asset_response(updated_asset)

        @router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
        def delete_asset(
            asset_id: UUID, use_case: DeleteAssetUseCase = Depends(delete_asset_use_case)
        ):
            use_case.execute(asset_id)
            return None

        return router
