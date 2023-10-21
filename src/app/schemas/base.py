from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ListModel(BaseModel, Generic[T]):
    items: list[T]
