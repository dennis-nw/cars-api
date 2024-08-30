from unittest.mock import patch

import pytest

from app.schemas.cars import CarMakeCreateSchema, CarModelCreateSchema
from app.service.cars import (
    fetch_car_makes,
    fetch_car_make,
    InvalidMakeException,
    add_car_make,
    fetch_model,
    fetch_make_models,
    add_make_models,
)
from tests.conftest import test_db, init_test_data


def test_fetch_car_makes(test_db, init_test_data):
    makes = fetch_car_makes(session=test_db)
    assert len(makes) == 4


def test_fetch_car_makes_with_search(test_db, init_test_data):
    makes = fetch_car_makes(session=test_db, search="b")
    assert len(makes) == 1


def test_fetch_car_make(test_db, init_test_data):
    make = fetch_car_make(session=test_db, make_id="bmw")
    assert make.id == "bmw"
    assert make.name == "BMW"


def test_fetch_car_make_does_not_exist(test_db, init_test_data):
    with pytest.raises(InvalidMakeException):
        fetch_car_make(session=test_db, make_id="tesla")


def test_add_car_make(test_db, init_test_data):
    assert len(fetch_car_makes(session=test_db)) == 4

    make = CarMakeCreateSchema(name="Lexus")
    new_make = add_car_make(session=test_db, car_make=make)
    assert new_make.id == "lexus"
    assert new_make.name == "Lexus"

    assert len(fetch_car_makes(session=test_db)) == 5

    added_make = fetch_car_make(session=test_db, make_id=new_make.id)
    assert added_make.id == "lexus"
    assert added_make.name == "Lexus"


@patch("app.service.cars.CarMake.create")
def test_add_car_make_already_exists(mock_create_car_make, test_db, init_test_data):
    make = CarMakeCreateSchema(name="Audi")

    assert len(fetch_car_makes(session=test_db)) == 4

    add_car_make(session=test_db, car_make=make)

    assert not mock_create_car_make.called

    assert len(fetch_car_makes(session=test_db)) == 4


def test_fetch_model(test_db, init_test_data):
    model = fetch_model(session=test_db, model_id="audi-q5")

    assert model.make_id == "audi"
    assert model.id == "audi-q5"
    assert model.name == "Q5"


def test_fetch_model_does_not_exist(test_db, init_test_data):
    model = fetch_model(session=test_db, model_id="abc")
    assert model is None


def test_fetch_make_models(test_db, init_test_data):
    models = fetch_make_models(session=test_db, make_id="audi")
    assert len(models) == 2


@patch("app.service.cars.CarModel.create")
def test_add_make_models(mock_model_create, test_db, init_test_data):
    models = [
        CarModelCreateSchema(name="Hilux"),
        CarModelCreateSchema(name="Starlet"),
        CarModelCreateSchema(name="Prado"),
    ]
    new_models = add_make_models(session=test_db, make_id="toyota", models=models)

    assert mock_model_create.call_count == 2
    assert len(new_models) == 3
