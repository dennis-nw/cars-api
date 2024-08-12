from app.service.cars import fetch_car_makes, fetch_car_make
from tests.conftest import test_db, init_test_data


def test_fetch_car_makes(test_db, init_test_data):
    makes = fetch_car_makes(session=test_db)
    assert len(makes) == 4


def test_fetch_car_make(test_db, init_test_data):
    make = fetch_car_make(session=test_db, make_id="bmw")
    assert make.id == "bmw"
    assert make.name == "BMW"
