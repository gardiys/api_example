import datetime

import pytest

from app.core.config import settings
from app.domain.examples import Example
from app.domain.filters import ExamplesFilter
from app.services.example import get_examples
from tests.repositories import StubExampleRepository


@pytest.mark.asyncio()
async def test_get_empty_examples():
    example_repository = StubExampleRepository(examples=[])
    filter = ExamplesFilter()
    result = await get_examples(filter=filter, example_repository=example_repository)
    assert result == []


@pytest.mark.asyncio()
async def test_get_examples():
    expected = [
        Example(
            id=1,
            name="1",
            description="1 description",
            created_at=datetime.datetime(
                year=2023,
                month=1,
                day=1,
                hour=12,
                minute=31,
                second=23,
                tzinfo=settings.tz,
            ),
            updated_at=datetime.datetime(
                year=2023,
                month=1,
                day=1,
                hour=12,
                minute=31,
                second=23,
                tzinfo=settings.tz,
            ),
        ),
        Example(
            id=2,
            name="2",
            description="2 description",
            created_at=datetime.datetime(
                year=2023,
                month=1,
                day=1,
                hour=12,
                minute=31,
                second=23,
                tzinfo=settings.tz,
            ),
            updated_at=datetime.datetime(
                year=2023,
                month=1,
                day=1,
                hour=12,
                minute=31,
                second=23,
                tzinfo=settings.tz,
            ),
        ),
    ]
    example_repository = StubExampleRepository(examples=expected)
    filter = ExamplesFilter()
    result = await get_examples(filter=filter, example_repository=example_repository)
    assert result == expected
