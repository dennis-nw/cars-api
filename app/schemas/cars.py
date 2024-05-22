from pydantic import BaseModel


class CarMakeBaseSchema(BaseModel):
    name: str


class CarMakeCreateSchema(CarMakeBaseSchema):
    pass


class CarMakeSchema(CarMakeBaseSchema):
    id: str


class CarModelBaseSchema(BaseModel):
    name: str


class CarModelCreateSchema(CarModelBaseSchema):
    pass


class CarModelSchema(CarModelBaseSchema):
    id: str
