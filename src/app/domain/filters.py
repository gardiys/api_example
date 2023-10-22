import datetime
from dataclasses import dataclass, field


@dataclass
class ExamplesFilter:
    example_ids: list[int] | None = field(default=None)
    created_before: datetime.date | None = field(default=None)
    created_after: datetime.date | None = field(default=None)
