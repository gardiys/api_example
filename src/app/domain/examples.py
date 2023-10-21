import datetime
from dataclasses import dataclass


@dataclass
class Example:
    id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
