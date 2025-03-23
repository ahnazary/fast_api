import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from sqlalchemy import text
from src.security import verify_password


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("test_user_1", "test123", 200),
        ("test_user_2", "test123456", 200),
    ],
)
def test_create_new_user(
    test_client, get_jwt_token, test_db, username, password, status_code
):
    response = test_client.post(
        "/users/create/",
        json={"username": username, "password": password},
        headers={"Authorization": f"Bearer {get_jwt_token}"},
    )
    user = test_db.execute(
        text(f"SELECT * FROM users where username = '{username}'")
    ).fetchone()

    assert response.status_code == status_code
    assert user is not None
    assert user[0] == username
    assert verify_password(password, user[1])
