from fastapi import status
from ..main import app
from ..models import Todos
from ..routers.todos import get_db, get_current_user
from .utils import *  # noqa: F403


app.dependency_overrides[get_db] = override_get_db  # noqa: F405
app.dependency_overrides[get_current_user] = override_get_current_user  # noqa: F405


def test_read_all_authenticated(test_todo):
    response = client.get("/")  # noqa: F405
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "complete": False,
            "title": "Learn to code",
            "description": "Need to learn everyday",
            "id": 1,
            "priority": 5,
            "owner_id": 1,
        }
    ]


def test_read_one_authenticated(test_todo):
    response = client.get("/todo/get-todo/1")  # noqa: F405
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "complete": False,
        "title": "Learn to code",
        "description": "Need to learn everyday",
        "id": 1,
        "priority": 5,
        "owner_id": 1,
    }


def test_read_one_authenticated_not_found():
    response = client.get("/todo/get-todo/999")  # noqa: F405
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(test_todo):
    request_data = {
        "title": "New Todo!",
        "description": "New todo description",
        "priority": 5,
        "complete": False,
    }

    response = client.post("/todo/create", json=request_data)  # noqa: F405
    assert response.status_code == 201
    db = TestingSessionLocal()  # noqa: F405
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(test_todo):
    request_data = {
        "title": "Change the title of the todo already saved!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todo/modify/1", json=request_data)  # noqa: F405
    assert response.status_code == 204
    db = TestingSessionLocal()  # noqa: F405
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "Change the title of the todo already saved!"


def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "Change the title of the todo already saved!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todo/modify/999", json=request_data)  # noqa: F405
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found."}


def test_delete_todo(test_todo):
    response = client.delete("todo/delete/1")  # noqa: F405
    assert response.status_code == 204
    db = TestingSessionLocal()  # noqa: F405
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete("todo/delete/999")  # noqa: F405
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found."}
