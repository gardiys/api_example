import copy
import datetime

from app.core.config import settings
from app.domain.examples import Example
from app.domain.filters import ExamplesFilter
from app.repositories.example import AbstractExampleRepository
from app.repositories.first_external import AbstractFirstExternalRepository
from app.repositories.second_external import AbstractSecondExternalRepository


class StubExampleRepository(AbstractExampleRepository):
    def __init__(self, examples: list[Example]):
        self.examples = examples
        self.commit_used = False

    async def get_all_examples(self, filter: ExamplesFilter) -> list[Example]:
        result = []
        for example in self.examples:
            if filter.example_ids and example.id not in filter.example_ids:
                continue
            if filter.created_before and example.created_at > filter.created_before:
                continue
            if filter.created_after and example.created_at < filter.created_after:
                continue
            result.append(copy.deepcopy(example))
        return result

    async def create_example(self, name: str, description: str) -> Example:
        example = Example(
            id=max([e.id for e in self.examples] or (0,)) + 1,
            name=name,
            description=description,
            created_at=datetime.datetime.now(tz=settings.tz),
            updated_at=datetime.datetime.now(tz=settings.tz),
        )
        self.examples.append(example)
        return example

    async def commit(self):
        self.commit_used = True


class StubFirstExternalRepository(AbstractFirstExternalRepository):
    def __init__(self, description_result_length: int = 1):
        self.description_result_length = description_result_length
        self.description = "a" * self.description_result_length

    async def get_description_by_name(self, name: str) -> str:
        return self.description


class StubSecondExternalRepository(AbstractSecondExternalRepository):
    def __init__(self, description_result_length: int = 1):
        self.description_result_length = description_result_length
        self.description = "b" * self.description_result_length

    async def get_description_by_name(self, name: str) -> str:
        return self.description
