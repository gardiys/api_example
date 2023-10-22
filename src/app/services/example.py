import asyncio

from app.domain.examples import Example
from app.domain.filters import ExamplesFilter
from app.repositories.example import AbstractExampleRepository
from app.repositories.first_external import AbstractFirstExternalRepository
from app.repositories.second_external import AbstractSecondExternalRepository


async def get_examples(
    filter: ExamplesFilter, example_repository: AbstractExampleRepository
) -> list[Example]:
    result = await example_repository.get_all_examples(filter=filter)
    return result


async def create_example(
    name: str,
    example_repository: AbstractExampleRepository,
    first_external_repository: AbstractFirstExternalRepository,
    second_external_repository: AbstractSecondExternalRepository,
) -> Example:
    first_description_result, second_description_result = await asyncio.gather(
        first_external_repository.get_description_by_name(name=name),
        second_external_repository.get_description_by_name(name=name),
    )
    if len(first_description_result) > len(second_description_result):
        description = first_description_result
    else:
        description = second_description_result

    example = await example_repository.create_example(
        name=name, description=description
    )
    await example_repository.commit()
    return example
