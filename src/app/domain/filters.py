import datetime
from dataclasses import dataclass


@dataclass
class ExamplesFilter:
    example_ids: list[int] | None
    created_before: datetime.date | None
    created_after: datetime.date | None
