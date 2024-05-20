from sqlalchemy import (
    String,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from app.db.active_record import ActiveRecordMixin


class Base(DeclarativeBase):
    pass


class CarMake(Base, ActiveRecordMixin):
    __tablename__ = "car_makes"

    id: Mapped[str] = mapped_column(String(100), primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class CarModel(Base, ActiveRecordMixin):
    __tablename__ = "car_models"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    make_id: Mapped[str] = mapped_column(String(100), ForeignKey("car_makes.id"))

    __table_args__ = (UniqueConstraint("name", "make_id"),)
