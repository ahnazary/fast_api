import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))


def test_login_user(test_client):
    """
    In this test, we are testing the login of a user.
    First we send a POST request to the /token endpoint with the username and password.
    Then we check if the response status code and the access token in the response are as expected.
    """
    response = test_client.post(
        "/auth/token",
        data={"username": "admin", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] is not None
