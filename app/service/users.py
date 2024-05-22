import bcrypt
from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.users import UserCreateSchema, UserAuthSchema, UserBaseSchema


def get_password_hash(password: str):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt)


def verify_password_hash(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def fetch_user(
    session: Session, user: UserCreateSchema, create_if_none: bool = False
) -> tuple[UserBaseSchema, bool]:
    created = False
    existing_user = User.find(session, user.email, "email")
    if existing_user is None and create_if_none:
        hashed_password = get_password_hash(user.password)
        new_user = User.create(session, email=user.email, password=hashed_password)
        return UserBaseSchema.from_orm(new_user), created
    return UserBaseSchema.from_orm(existing_user), created


def authenticate_user(session: Session, user: UserAuthSchema):
    user = User.find(session, user.email, "email")
    if user is None:
        return False
    if not verify_password_hash(user.password, user.password):
        return False
    return user
