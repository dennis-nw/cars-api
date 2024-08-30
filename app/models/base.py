from typing import Any, Self

from sqlalchemy import sql
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session


class Base(DeclarativeBase):
    pass


class ActiveRecordMixin:
    @classmethod
    def find(cls, session: Session, value: Any, key: str = "id") -> Self | None:
        params = {key: value}
        return cls.find_by(session, **params)

    @classmethod
    def find_by(cls, session: Session, **params: Any) -> Self | None:
        query = sql.select(cls).filter_by(**params)
        res = session.execute(query)
        return res.scalars().unique().one_or_none()

    @classmethod
    def create(cls, session: Session, autocommit: bool = True, **values: Any):
        instance = cls()
        instance.fill(**values)
        return instance.save(session, autocommit)

    def update(self, session: Session, autocommit: bool = True, **values: Any):
        updated = self.fill(**values)
        return updated.save(session, autocommit)

    def fill(self, **values: Any) -> Self:
        for col, value in values.items():
            if not hasattr(self, col):
                raise Exception(f"{self} has no attribute {col}")
            setattr(self, col, value)
        return self

    def save(self, session: Session, autocommit: bool = True) -> Self:
        session.add(self)
        if autocommit:
            session.commit()
        return self
