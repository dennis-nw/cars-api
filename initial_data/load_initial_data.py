import csv
import os

from slugify import slugify

from app.db import session_scope
from app.models import CarModel, CarMake


def get_car_makes_from_csv():
    with open(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "initial_data.csv"))
    ) as car_makes:
        reader = csv.reader(car_makes)
        for row in reader:
            yield row


def add_car_makes():
    added_makes = set()
    with session_scope() as session:
        for make in get_car_makes_from_csv():
            if make[0] not in added_makes:
                new_make = CarMake.create(
                    session, id=slugify(make[0]), name=make[0]
                )
                added_makes.add(make[0])
            CarModel.create(
                session,
                id=f"{slugify(make[0])}-{slugify(make[1])}",
                name=make[1],
                make_id=new_make.id,
            )
    print("Done.")


if __name__ == "__main__":
    add_car_makes()
