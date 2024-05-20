from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models as db


class InvalidMakeException(Exception):
    def __init__(self, make_id: str):
        self.make_id = make_id
        self.message = f"Invalid car make - {make_id}"
        super().__init__(self.message)


def fetch_car_makes(session: Session, search: str = None):
    stmt = select(db.CarMake)
    if search:
        stmt = stmt.where(db.CarMake.name.istartswith(search))
    res = session.execute(stmt)
    return res.scalars().all()


def fetch_car_make(session: Session, make_id: str):
    make = db.CarMake.find(session, value=make_id)
    if make is None:
        raise InvalidMakeException(make_id)
    return make


def fetch_make_models(session: Session, make_id: str):
    if fetch_car_make(session, make_id) is None:
        raise InvalidMakeException(make_id)
    stmt = select(db.CarModel).where(db.CarModel.make_id == make_id)
    res = session.execute(stmt)
    return res.scalars().all()
