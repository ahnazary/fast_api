import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from sqlalchemy import text


@pytest.mark.parametrize(
    "customer_id, name, expected_status_code, expected_customer_id, expected_name",
    [
        (5, "Bob", 200, 5, "Bob"),
        (6, "Charlie", 200, 6, "Charlie"),
    ],
)
def test_create_new_customer(
    test_client,
    get_jwt_token,
    test_db,
    customer_id,
    name,
    expected_status_code,
    expected_customer_id,
    expected_name,
):
    """
    In this test, we are testing the creation of a new customer.
    First we send a POST request to the /customers/ endpoint with the name.
    Then we check if the response status code and the name in the response are as expected.
    We also check if the customer was created in the database with the correct name.
    """
    response = test_client.post(
        "/customers/create/",
        json={"name": name, "id": customer_id},
        headers={"Authorization": f"Bearer {get_jwt_token}"},
    )
    assert response.status_code == expected_status_code
    assert response.json()["name"] == expected_name
    assert response.json()["id"] == expected_customer_id

    customer = test_db.execute(
        text(f"SELECT * FROM customers where id = {response.json()['id']}")
    ).fetchone()
    assert customer is not None
    assert customer[1] == name
    assert customer[0] == customer_id
