from abc import ABC, abstractmethod

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.domain.examples import Example
from app.domain.filters import ExamplesFilter


class AbstractExampleRepository(ABC):
    @abstractmethod
    async def get_all_examples(self, filter: ExamplesFilter) -> list[Example]:
        pass


class SQLExampleRepository(AbstractExampleRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_examples(self, filter: ExamplesFilter) -> list[Example]:
        filters = []
        if filter.example_ids is not None:
            filters.append(models.Examples.id.in_(filter.example_ids))
        if filter.created_before is not None:
            filters.append(models.Examples.created_at <= filter.created_before)
        if filter.created_after is not None:
            filters.append(models.Examples.created_at >= filter.created_after)

        q = select(
            models.Examples.id,
            models.Examples.name,
            models.Examples.created_at,
            models.Examples.updated_at,
        ).where(and_(*filters))
        raw_result = await self.db_session.execute(q)

        data = []
        for example in raw_result.all():
            data.append(
                Example(
                    id=example.id,
                    name=example.name,
                    created_at=example.created_at,
                    updated_at=example.updated_at,
                )
            )
        return data
