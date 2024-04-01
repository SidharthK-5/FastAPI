from fastapi import status
from .utils import *  # noqa: F403
from ..routers.admin import get_db, get_current_user
from ..models import Todos


app.dependency_overrides[get_db] = override_get_db  # noqa: F405
app.dependency_overrides[get_current_user] = override_get_current_user  # noqa: F405


def test_admin_read_all_authenticated(test_todo):
    response = client.get("admin/todo")  # noqa: F405
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


def test_admin_delete_todo(test_todo):
    response = client.delete("admin/todo/1")  # noqa: F405
    assert response.status_code == 204

    db = TestingSessionLocal()  # noqa: F405
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("admin/todo/9999")  # noqa: F405
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
