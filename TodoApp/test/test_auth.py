from .utils import *  # noqa: F403
from ..routers.auth import get_db, authenticate_user

app.dependency_overrides[get_db] = override_get_db  # noqa: F405


def test_authenticate_user(test_user):
    db = TestingSessionLocal()  # noqa: F405

    authenticated_user = authenticate_user(
        username=test_user.username, password="testpassword", db=db
    )
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user("WronhUserName", "testpassword", db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, "wrongpassword", db)
    assert wrong_password_user is False
