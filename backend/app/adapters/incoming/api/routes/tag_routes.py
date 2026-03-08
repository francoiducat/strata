from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.application.use_cases.tag.create_tag import CreateTagCommand, CreateTagUseCase
from app.application.use_cases.tag.get_all_tags import GetAllTagsUseCase
from app.application.use_cases.tag.get_tag import GetTagUseCase
from app.application.use_cases.tag.delete_tag import DeleteTagUseCase
from app.adapters.incoming.api.dependencies.tags import (
    create_tag_use_case,
    get_all_tags_use_case,
    get_tag_use_case,
    delete_tag_use_case,
)
from app.adapters.incoming.api.mappers.api_mapper import ApiMapper
from app.adapters.incoming.api.schemas.tag_request import TagCreateRequest
from app.adapters.incoming.api.schemas.tag_response import TagResponse
from app.adapters.incoming.api.schemas.error_response import ErrorResponse


class TagRoutes:

    @staticmethod
    def get_router() -> APIRouter:
        router = APIRouter(prefix="/tags", tags=["Tags"])

        @router.get("/", response_model=List[TagResponse])
        def get_all_tags(
            use_case: GetAllTagsUseCase = Depends(get_all_tags_use_case),
        ):
            tags = use_case.execute()
            return ApiMapper.to_tag_response_list(tags)

        @router.post(
            "/",
            response_model=TagResponse,
            status_code=status.HTTP_201_CREATED,
            responses={409: {"model": ErrorResponse}},
        )
        def create_tag(
            request: TagCreateRequest,
            use_case: CreateTagUseCase = Depends(create_tag_use_case),
        ):
            tag = use_case.execute(CreateTagCommand(name=request.name))
            return ApiMapper.to_tag_response(tag)

        @router.get(
            "/{tag_id}",
            response_model=TagResponse,
            responses={404: {"model": ErrorResponse}},
        )
        def get_tag(
            tag_id: UUID,
            use_case: GetTagUseCase = Depends(get_tag_use_case),
        ):
            tag = use_case.execute(tag_id)
            return ApiMapper.to_tag_response(tag)

        @router.delete(
            "/{tag_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            responses={404: {"model": ErrorResponse}},
        )
        def delete_tag(
            tag_id: UUID,
            use_case: DeleteTagUseCase = Depends(delete_tag_use_case),
        ):
            use_case.execute(tag_id)
            return None

        return router
