from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    email: str

    class Config:
        from_attributes = True


class UserCreateSchema(UserBaseSchema):
    password: str


class UserAuthSchema(UserCreateSchema):
    pass
