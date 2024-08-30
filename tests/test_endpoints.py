from slugify import slugify
from starlette import status

from tests.conftest import client, init_test_data


def test_get_car_makes(client, init_test_data):
    response = client.get("/makes")
    assert len(response.json()) == 4
    assert response.status_code == 200


def test_add_new_car_make(client):
    make_name = "BYD"
    response = client.post(url="/makes", json={"name": make_name})

    expected_response = {"id": slugify(make_name), "name": make_name}

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response


def test_get_non_existent_car_make_returns_404(client):
    response = client.get(url="/makes/xyz")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_car_make(client, init_test_data):
    response = client.get(url="/makes/audi")

    expected_response = {"id": "audi", "name": "Audi"}

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


def test_get_make_models(client, init_test_data):
    response = client.get(url="/makes/audi/models")
    expected_response = [
        {"id": "audi-a4", "name": "A4"},
        {"id": "audi-q5", "name": "Q5"},
    ]
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


def test_add_new_make_model_invalid_make(client):
    response = client.post(url="makes/xyz/models", json=[{"name": "Prado"}])
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_add_new_make_model(client, init_test_data):
    response = client.post(url="/makes/infinity/models", json=[{"name": "Q60"}])
    expected_response = [{"id": "infinity-q60", "name": "Q60"}]
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_response
