from pydantic import BaseModel


class CarMakeBase(BaseModel):
    name: str


class CarMakeCreate(CarMakeBase):
    pass


class CarMake(CarMakeBase):
    id: str


class CarModelBase(BaseModel):
    name: str


class CarModelCreate(CarModelBase):
    pass


class CarModel(CarModelBase):
    id: str
