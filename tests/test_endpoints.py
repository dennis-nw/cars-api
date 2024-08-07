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
