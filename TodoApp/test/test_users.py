from .utils import *  # noqa: F403
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db  # noqa: F405
app.dependency_overrides[get_current_user] = override_get_current_user  # noqa: F405

def test_return_user(test_user):
    response = client.get("/user/get-details")  # noqa: F405
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "Sid5"
    assert response.json()["email"] == "sid5@gmail.com"
    assert response.json()["first_name"] == "Sid"
    assert response.json()["last_name"] == "K"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "(111)-111-1111"