import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from sqlalchemy import text


@pytest.mark.parametrize(
    "customer_id, initial_deposit, expected_status_code, expected_balance",
    [
        (1, 100.0, 200, 100.0),
        (2, 200.0, 200, 200.0),
    ],
)
def test_create_new_account(
    test_client,
    get_jwt_token,
    test_db,
    customer_id,
    initial_deposit,
    expected_status_code,
    expected_balance,
):
    """
    In this test, we are testing the creation of a new account.
    First we send a POST request to the /accounts/ endpoint with the customer_id
    and initial_deposit.
    Then we check if the response status code and the balance in the response are as expected.
    We also check if the account was created in the database with the correct customer_id
    and initial_deposit.
    """
    response = test_client.post(
        "/accounts/create/",
        json={"customer_id": customer_id, "initial_deposit": initial_deposit},
        headers={"Authorization": f"Bearer {get_jwt_token}"},
    )
    assert response.status_code == expected_status_code
    assert response.json()["balance"] == expected_balance

    account = test_db.execute(
        text(f"SELECT * FROM accounts where id = {response.json()['account_id']}")
    ).fetchone()
    assert account is not None
    assert account[1] == customer_id
    assert account[2] == initial_deposit


@pytest.mark.parametrize(
    "customer_id, initial_deposit",
    [
        (5, 100.0),
        (6, 200.0),
    ],
)
def test_create_acoount_for_customer_not_found(
    get_jwt_token, test_client, customer_id, initial_deposit
):
    """
    In this test, we are testing the creation of a new account for a customer that does not exist.
    We send a POST request to the /accounts/ endpoint with the customer_id that does not exist.
    We expect an exception to be raised.
    """
    with pytest.raises(Exception):
        test_client.post(
            "/accounts/create/",
            json={"customer_id": customer_id, "initial_deposit": initial_deposit},
            headers={"Authorization": f"Bearer {get_jwt_token}"},
        )


@pytest.mark.parametrize(
    "account_id, expected_status_code, expected_balance",
    [
        (1, 200, 1000.0),
        (2, 200, 1500.0),
        (3, 200, 2000.0),
        (4, 200, 2500.0),
    ],
)
def test_get_balance(
    test_client,
    get_jwt_token,
    test_db,
    account_id,
    expected_status_code,
    expected_balance,
):
    """
    In this test, we are testing the get balance endpoint.
    We send a GET request to the /accounts/{account_id}/balance/ endpoint with the account_id
    and compare the deposit in the response with the expected deposit.
    """
    response = test_client.get(
        f"/accounts/{account_id}/balance/",
        headers={"Authorization": f"Bearer {get_jwt_token}"},
    )
    assert response.status_code == expected_status_code
    assert response.json()["balance"] == expected_balance
    assert response.json()["account_id"] == account_id

    # check if the in the database is also correct
    account = test_db.execute(
        text(f"SELECT * FROM accounts where id = {account_id}")
    ).fetchone()
    assert account is not None
    assert account[2] == expected_balance


@pytest.mark.parametrize(
    "customer_id, expected_status_code",
    [
        (5, 404),
        (6, 404),
    ],
)
def test_get_balance_account_not_found(
    test_client, get_jwt_token, customer_id, expected_status_code
):
    """
    In this test, we are testing the get balance endpoint when the account is not found.
    We send a GET request to the /accounts/{account_id}/balance/ endpoint with the account_id.
    We check if the response status is 404 and the detail in the response is "Account not found".
    """
    response = test_client.get(
        f"/accounts/{customer_id}/balance/",
        headers={"Authorization": f"Bearer {get_jwt_token}"},
    )
    assert response.status_code == expected_status_code
    assert response.json()["detail"] == "Account not found"
