import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from sqlalchemy import text
from src.security import hash_password


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("test_user_1", "test123", 200),
        ("test_user_2", "test123456", 200),
    ],
)
def test_create_new_user(
    get_jwt_token, test_db, test_client, username, password, status_code
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
    assert user[1] == hash_password(password)
