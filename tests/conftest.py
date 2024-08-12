import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app.db.session import get_db_session
from app.main import app
from app.models.cars import CarMake, CarModel

DATABASE_URL = "sqlite:///data/test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="module")
def test_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db_session():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db_session] = override_get_db_session

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def init_test_data(test_db):
    car_makes = [
        CarMake(id="audi", name="Audi"),
        CarMake(id="bmw", name="BMW"),
        CarMake(id="infinity", name="Infinity"),
        CarMake(id="toyota", name="Toyota"),
    ]
    car_models = [
        CarModel(id="audi-q5", name="Q5", make_id="audi"),
        CarModel(id="audi-a4", name="A4", make_id="audi"),
        CarModel(id="infinity-q50", name="Q50", make_id="infinity"),
        CarModel(id="toyota-prado", name="Prado", make_id="toyota"),
    ]
    test_db.add_all(car_makes)
    test_db.add_all(car_models)
    test_db.commit()

    yield

    test_db.query(CarMake).delete()
    test_db.query(CarModel).delete()
    test_db.commit()
