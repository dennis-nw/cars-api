from pydantic import BaseModel


class CarMake(BaseModel):
    id: str
    name: str


class CarModel(BaseModel):
    id: str
    name: str
