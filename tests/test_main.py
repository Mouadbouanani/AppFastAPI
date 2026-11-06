from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo API is running"}


def test_create_and_list_task():
    task = {"id": 1, "title": "Buy milk", "done": False}
    response = client.post("/tasks", json=task)
    assert response.status_code == 200
    assert response.json()["title"] == "Buy milk"

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404
