import pytest

from app.services.example import create_example
from tests.repositories import (
    StubExampleRepository,
    StubFirstExternalRepository,
    StubSecondExternalRepository,
)


@pytest.mark.asyncio()
async def test_create_example():
    example_repository = StubExampleRepository(examples=[])
    first_external_repository = StubFirstExternalRepository()
    second_external_repository = StubSecondExternalRepository()
    name = "my name"

    await create_example(
        name=name,
        example_repository=example_repository,
        first_external_repository=first_external_repository,
        second_external_repository=second_external_repository,
    )
    actual_example = example_repository.examples[0]
    assert actual_example
    assert actual_example.name == name
    assert actual_example.description


@pytest.mark.asyncio()
async def test_create_exampel_first_description_longer():
    example_repository = StubExampleRepository(examples=[])
    first_external_repository = StubFirstExternalRepository(description_result_length=4)
    second_external_repository = StubSecondExternalRepository()
    name = "my name"

    await create_example(
        name=name,
        example_repository=example_repository,
        first_external_repository=first_external_repository,
        second_external_repository=second_external_repository,
    )
    actual_example = example_repository.examples[0]
    assert actual_example.description == first_external_repository.description


@pytest.mark.asyncio()
async def test_create_exampel_second_description_longer():
    example_repository = StubExampleRepository(examples=[])
    first_external_repository = StubFirstExternalRepository()
    second_external_repository = StubSecondExternalRepository(
        description_result_length=4
    )
    name = "my name"

    await create_example(
        name=name,
        example_repository=example_repository,
        first_external_repository=first_external_repository,
        second_external_repository=second_external_repository,
    )
    actual_example = example_repository.examples[0]
    assert actual_example.description == second_external_repository.description
