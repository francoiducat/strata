from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.application.use_cases.portfolio.create_portfolio import (
    CreatePortfolioCommand,
    CreatePortfolioUseCase,
)
from app.application.use_cases.portfolio.get_portfolio import GetPortfolioUseCase
from app.application.use_cases.portfolio.delete_portfolio import DeletePortfolioUseCase
from app.application.use_cases.portfolio.get_all_portfolios import GetAllPortfoliosUseCase
from app.application.use_cases.portfolio.take_portfolio_snapshot import TakePortfolioSnapshotUseCase
from app.application.use_cases.portfolio.get_portfolio_snapshots import GetPortfolioSnapshotsUseCase
from app.application.use_cases.portfolio.update_portfolio import UpdatePortfolioCommand, UpdatePortfolioUseCase
from app.adapters.incoming.api.dependencies.portfolios import (
    create_portfolio_use_case,
    get_portfolio_use_case,
    delete_portfolio_use_case,
    get_all_portfolios_use_case,
    take_portfolio_snapshot_use_case,
    get_portfolio_snapshots_use_case,
    update_portfolio_use_case,
)
from app.adapters.incoming.api.mappers.api_mapper import ApiMapper
from app.adapters.incoming.api.schemas.portfolio_request import PortfolioCreateRequest, PortfolioUpdateRequest
from app.adapters.incoming.api.schemas.portfolio_response import PortfolioResponse
from app.adapters.incoming.api.schemas.portfolio_snapshot_response import PortfolioSnapshotResponse
from app.adapters.incoming.api.schemas.error_response import ErrorResponse


class PortfolioRoutes:

    @staticmethod
    def get_router() -> APIRouter:
        router = APIRouter(prefix="/portfolios", tags=["Portfolios"])

        @router.post("/", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
        def create_portfolio(
            request: PortfolioCreateRequest,
            create_use_case: CreatePortfolioUseCase = Depends(create_portfolio_use_case),
        ) -> PortfolioResponse:
            command = CreatePortfolioCommand(**request.model_dump())
            created = create_use_case.execute(command)
            return ApiMapper.to_portfolio_response(created)

        @router.get("/", response_model=list[PortfolioResponse])
        def get_all_portfolios(
            use_case: GetAllPortfoliosUseCase = Depends(get_all_portfolios_use_case),
        ) -> list[PortfolioResponse]:
            portfolios = use_case.execute()
            return [ApiMapper.to_portfolio_response(p) for p in portfolios]

        @router.get("/{portfolio_id}", response_model=PortfolioResponse)
        def get_portfolio(
            portfolio_id: UUID, use_case: GetPortfolioUseCase = Depends(get_portfolio_use_case)
        ) -> PortfolioResponse:
            portfolio = use_case.execute(portfolio_id)
            return ApiMapper.to_portfolio_response(portfolio)

        @router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
        def delete_portfolio(
            portfolio_id: UUID, use_case: DeletePortfolioUseCase = Depends(delete_portfolio_use_case)
        ):
            use_case.execute(portfolio_id)
            return None

        @router.post(
            "/{portfolio_id}/snapshots",
            response_model=PortfolioSnapshotResponse,
            status_code=status.HTTP_201_CREATED,
        )
        def take_portfolio_snapshot(
            portfolio_id: UUID,
            use_case: TakePortfolioSnapshotUseCase = Depends(take_portfolio_snapshot_use_case),
        ) -> PortfolioSnapshotResponse:
            snapshot = use_case.execute(portfolio_id)
            return ApiMapper.to_portfolio_snapshot_response(snapshot)

        @router.get("/{portfolio_id}/snapshots", response_model=list[PortfolioSnapshotResponse])
        def get_portfolio_snapshots(
            portfolio_id: UUID,
            use_case: GetPortfolioSnapshotsUseCase = Depends(get_portfolio_snapshots_use_case),
        ) -> list[PortfolioSnapshotResponse]:
            portfolio = use_case.execute(portfolio_id)
            return ApiMapper.to_portfolio_snapshot_response_list(portfolio.snapshots or [])

        @router.put("/{portfolio_id}", response_model=PortfolioResponse, responses={404: {"model": ErrorResponse}})
        def update_portfolio(
            portfolio_id: UUID,
            request: PortfolioUpdateRequest,
            use_case: UpdatePortfolioUseCase = Depends(update_portfolio_use_case),
        ) -> PortfolioResponse:
            command = UpdatePortfolioCommand(portfolio_id=portfolio_id, **request.model_dump())
            updated = use_case.execute(command)
            return ApiMapper.to_portfolio_response(updated)

        return router
