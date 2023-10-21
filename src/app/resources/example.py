import datetime

from fastapi import APIRouter, Query

from app.core.database import async_session
from app.domain.examples import Example
from app.domain.filters import ExamplesFilter
from app.repositories.example import SQLExampleRepository
from app.repositories.first_external import HTTPFirstExternalRepository
from app.repositories.second_external import HTTPSecondExternalRepository
from app.schemas.base import ListModel
from app.schemas.example import CreateExample, GetExampleModel
from app.services import example as example_service

router = APIRouter()


@router.get("", response_model=ListModel[GetExampleModel])
async def get_users(
    example_ids: list[int] | None = Query(default=None),  # noqa: B008
    created_before: datetime.date | None = Query(default=None),  # noqa: B008
    created_after: datetime.date | None = Query(default=None),  # noqa: B008
) -> dict[str, list[Example]]:
    async with async_session() as session:
        examples = await example_service.get_examples(
            filter=ExamplesFilter(
                example_ids=example_ids,
                created_before=created_before,
                created_after=created_after,
            ),
            example_repository=SQLExampleRepository(db_session=session),
        )
        return {"items": examples}


@router.post("", response_model=GetExampleModel)
async def create_example(example: CreateExample):
    async with async_session() as session:
        example = await example_service.create_example(
            name=example.name,
            example_repository=SQLExampleRepository(db_session=session),
            first_external_service=HTTPFirstExternalRepository(),
            second_external_service=HTTPSecondExternalRepository(),
        )
        return example
