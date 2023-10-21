from pydantic import BaseModel


class GetExampleModel(BaseModel):
    id: int
    name: str
