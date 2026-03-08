from typing import List, Optional
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
from app.application.use_cases.asset.dispose_asset import DisposeAssetUseCase
from app.application.use_cases.asset.get_assets_by_portfolio import GetAssetsByPortfolioUseCase
from app.application.use_cases.asset_snapshot.create_asset_snapshot import CreateAssetSnapshotUseCase
from app.application.use_cases.asset_snapshot.get_asset_snapshots import GetAssetSnapshotsUseCase
from app.application.use_cases.tag.add_tag_to_asset import AddTagToAssetCommand, AddTagToAssetUseCase
from app.application.use_cases.tag.remove_tag_from_asset import RemoveTagFromAssetCommand, RemoveTagFromAssetUseCase
from app.application.use_cases.category.add_asset_to_category import AddAssetToCategoryCommand, AddAssetToCategoryUseCase
from app.application.use_cases.category.remove_asset_from_category import RemoveAssetFromCategoryCommand, RemoveAssetFromCategoryUseCase
from app.adapters.incoming.api.dependencies.assets import (
    create_asset_use_case,
    get_all_assets_use_case,
    get_asset_use_case,
    update_asset_use_case,
    delete_asset_use_case,
    dispose_asset_use_case,
    get_assets_by_portfolio_use_case,
)
from app.adapters.incoming.api.dependencies.asset_snapshots import (
    create_asset_snapshot_use_case,
    get_asset_snapshots_use_case,
)
from app.adapters.incoming.api.dependencies.tags import (
    add_tag_to_asset_use_case,
    remove_tag_from_asset_use_case,
)
from app.adapters.incoming.api.dependencies.categories import (
    add_asset_to_category_use_case,
    remove_asset_from_category_use_case,
)
from app.adapters.incoming.api.mappers.api_mapper import ApiMapper
from app.adapters.incoming.api.schemas.asset_request import AssetCreateRequest, AssetUpdateRequest
from app.adapters.incoming.api.schemas.asset_response import AssetResponse
from app.adapters.incoming.api.schemas.asset_snapshot_request import AssetSnapshotCreateRequest
from app.adapters.incoming.api.schemas.asset_snapshot_response import AssetSnapshotResponse
from app.adapters.incoming.api.schemas.error_response import ErrorResponse

class AssetRoutes:

    @staticmethod
    def get_router() -> APIRouter:
        router = APIRouter(prefix="/assets", tags=["Assets"])

        @router.get("/", response_model=List[AssetResponse])
        def get_all_assets(
            portfolio_id: Optional[UUID] = None,
            get_all_use_case: GetAllAssetsUseCase = Depends(get_all_assets_use_case),
            get_by_portfolio_use_case: GetAssetsByPortfolioUseCase = Depends(get_assets_by_portfolio_use_case),
        ):
            if portfolio_id:
                assets = get_by_portfolio_use_case.execute(portfolio_id)
            else:
                assets = get_all_use_case.execute()
            return ApiMapper.to_asset_response_list(assets)

        @router.get("/{asset_id}", response_model=AssetResponse, responses={404: {"model": ErrorResponse}})
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

        @router.put("/{asset_id}", response_model=AssetResponse, responses={404: {"model": ErrorResponse}})
        def update_asset(
            asset_id: UUID,
            request: AssetUpdateRequest,
            use_case: UpdateAssetUseCase = Depends(update_asset_use_case),
        ):
            """Update an existing asset's attributes."""
            command = UpdateAssetCommand(asset_id=asset_id, **request.model_dump())
            updated_asset = use_case.execute(command)
            return ApiMapper.to_asset_response(updated_asset)

        @router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"model": ErrorResponse}})
        def delete_asset(
            asset_id: UUID, use_case: DeleteAssetUseCase = Depends(delete_asset_use_case)
        ):
            use_case.execute(asset_id)
            return None

        @router.put("/{asset_id}/dispose", response_model=AssetResponse, responses={404: {"model": ErrorResponse}})
        def dispose_asset(
            asset_id: UUID,
            use_case: DisposeAssetUseCase = Depends(dispose_asset_use_case),
        ):
            asset = use_case.execute(asset_id)
            return ApiMapper.to_asset_response(asset)

        @router.get("/{asset_id}/snapshots", response_model=List[AssetSnapshotResponse], responses={404: {"model": ErrorResponse}})
        def get_asset_snapshots(
            asset_id: UUID,
            use_case: GetAssetSnapshotsUseCase = Depends(get_asset_snapshots_use_case),
        ):
            snapshots = use_case.execute(asset_id)
            return ApiMapper.to_asset_snapshot_response_list(snapshots)

        @router.post("/{asset_id}/snapshots", response_model=AssetSnapshotResponse, status_code=status.HTTP_201_CREATED, responses={404: {"model": ErrorResponse}})
        def create_asset_snapshot(
            asset_id: UUID,
            request: AssetSnapshotCreateRequest,
            use_case: CreateAssetSnapshotUseCase = Depends(create_asset_snapshot_use_case),
        ):
            snapshot = use_case.execute(
                asset_id=str(asset_id),
                value=request.value,
                observed_at=request.observed_at,
            )
            return ApiMapper.to_asset_snapshot_response(snapshot)

        @router.post("/{asset_id}/tags/{tag_id}", response_model=AssetResponse, responses={404: {"model": ErrorResponse}})
        def add_tag_to_asset(
            asset_id: UUID,
            tag_id: UUID,
            use_case: AddTagToAssetUseCase = Depends(add_tag_to_asset_use_case),
        ):
            asset = use_case.execute(AddTagToAssetCommand(asset_id=asset_id, tag_id=tag_id))
            return ApiMapper.to_asset_response(asset)

        @router.delete("/{asset_id}/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"model": ErrorResponse}})
        def remove_tag_from_asset(
            asset_id: UUID,
            tag_id: UUID,
            use_case: RemoveTagFromAssetUseCase = Depends(remove_tag_from_asset_use_case),
        ):
            use_case.execute(RemoveTagFromAssetCommand(asset_id=asset_id, tag_id=tag_id))
            return None

        @router.post("/{asset_id}/categories/{category_id}", response_model=AssetResponse, responses={404: {"model": ErrorResponse}})
        def add_category_to_asset(
            asset_id: UUID,
            category_id: UUID,
            use_case: AddAssetToCategoryUseCase = Depends(add_asset_to_category_use_case),
        ):
            asset = use_case.execute(AddAssetToCategoryCommand(asset_id=asset_id, category_id=category_id))
            return ApiMapper.to_asset_response(asset)

        @router.delete("/{asset_id}/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"model": ErrorResponse}})
        def remove_category_from_asset(
            asset_id: UUID,
            category_id: UUID,
            use_case: RemoveAssetFromCategoryUseCase = Depends(remove_asset_from_category_use_case),
        ):
            use_case.execute(RemoveAssetFromCategoryCommand(asset_id=asset_id, category_id=category_id))
            return None

        return router

