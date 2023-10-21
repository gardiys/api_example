import datetime

from fastapi import APIRouter, Query

from app.core.database import async_session
from app.domain.examples import Example
from app.domain.filters import ExamplesFilter
from app.repositories.example import SQLExampleRepository
from app.schemas.base import ListModel
from app.schemas.example import GetExampleModel
from app.services import example as example_service

router = APIRouter()


@router.get("", response_model=ListModel[GetExampleModel])
async def get_users(
    example_ids: list[int] | None = Query(default=None),  # noqa: B008
    created_before: datetime.date | None = Query(default=None),  # noqa: B008
    created_after: datetime.date | None = Query(default=None),  # noqa: B008
) -> dict[str, list[Example]]:
    async with async_session() as session:
        users = await example_service.get_examples(
            filter=ExamplesFilter(
                example_ids=example_ids,
                created_before=created_before,
                created_after=created_after,
            ),
            example_repository=SQLExampleRepository(db_session=session),
        )
        return {"items": users}
