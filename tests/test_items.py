import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routes.items import _reset_store

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clean_store() -> None:
    _reset_store()


def test_create_item_returns_201_and_item() -> None:
    response = client.post("/items", json={"name": "pen", "description": "blue ink"})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "pen", "description": "blue ink"}


def test_create_item_validation_error_when_name_missing() -> None:
    response = client.post("/items", json={"description": "no name"})

    assert response.status_code == 422


def test_list_items_empty_returns_empty_list() -> None:
    response = client.get("/items")

    assert response.status_code == 200
    assert response.json() == []


def test_list_items_returns_all_created() -> None:
    client.post("/items", json={"name": "a"})
    client.post("/items", json={"name": "b"})

    response = client.get("/items")

    assert response.status_code == 200
    assert [item["name"] for item in response.json()] == ["a", "b"]


def test_get_item_returns_item() -> None:
    client.post("/items", json={"name": "pen"})

    response = client.get("/items/1")

    assert response.status_code == 200
    assert response.json()["name"] == "pen"


def test_get_item_returns_404_when_missing() -> None:
    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_update_item_replaces_fields() -> None:
    client.post("/items", json={"name": "pen", "description": "blue"})

    response = client.put("/items/1", json={"name": "pencil", "description": "HB"})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "pencil", "description": "HB"}


def test_update_item_returns_404_when_missing() -> None:
    response = client.put("/items/999", json={"name": "ghost"})

    assert response.status_code == 404


def test_delete_item_returns_204_and_removes() -> None:
    client.post("/items", json={"name": "pen"})

    response = client.delete("/items/1")
    assert response.status_code == 204

    follow_up = client.get("/items/1")
    assert follow_up.status_code == 404


def test_delete_item_returns_404_when_missing() -> None:
    response = client.delete("/items/999")

    assert response.status_code == 404
