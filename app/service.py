from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models as db
from app import schemas
from app.models import CarMake, CarModel


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


def fetch_car_make(session: Session, make_id: str, raise_error: bool = True):
    make = db.CarMake.find(session, value=make_id)
    if make is None and raise_error:
        raise InvalidMakeException(make_id)
    return make


def add_car_make(session: Session, car_make: schemas.CarMakeCreate):
    make_id = slugify(car_make.name)
    existing_car_make = fetch_car_make(session, make_id, False)
    if existing_car_make is not None:
        return existing_car_make
    return CarMake.create(session=session, id=make_id, name=car_make.name)


def fetch_model(session: Session, model_id: str):
    return db.CarModel.find(session, model_id)


def fetch_make_models(session: Session, make_id: str):
    fetch_car_make(session, make_id)
    stmt = select(db.CarModel).where(db.CarModel.make_id == make_id)
    res = session.execute(stmt)
    return res.scalars().all()


def add_make_models(
    session: Session, make_id: str, models: list[schemas.CarModelCreate]
):
    if fetch_car_make(session, make_id) is None:
        raise InvalidMakeException(make_id)
    added_models: list[schemas.CarModel] = []
    for model in models:
        model_id = slugify(model.name)
        existing_model = fetch_model(session, model_id)
        if existing_model is None:
            new_model = CarModel.create(
                session, id=model_id, name=model.name, make_id=make_id
            )
            added_models.append(new_model)
        else:
            added_models.append(existing_model)
    return added_models
