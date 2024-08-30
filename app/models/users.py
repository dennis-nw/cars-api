from sqlalchemy import Integer, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, ActiveRecordMixin


class User(Base, ActiveRecordMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
