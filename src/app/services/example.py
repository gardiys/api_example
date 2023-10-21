from app.domain.examples import Example
from app.domain.filters import ExamplesFilter
from app.repositories.example import AbstractExampleRepository


async def get_examples(
    filter: ExamplesFilter, example_repository: AbstractExampleRepository
) -> list[Example]:
    result = await example_repository.get_all_examples(filter=filter)
    return result
