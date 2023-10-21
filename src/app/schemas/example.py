from pydantic import BaseModel


class GetExampleModel(BaseModel):
    id: int
    name: str


class CreateExample(BaseModel):
    name: str
