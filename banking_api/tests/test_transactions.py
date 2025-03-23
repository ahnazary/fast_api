import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from sqlalchemy import text


@pytest.mark.parametrize(
    "sender_account_id, receiver_account_id, amount, expected_status_code",
    [
        (1, 2, 100.0, 200),
        (3, 4, 200.0, 200),
    ],
)
def test_transfer_funds(
    test_client,
    get_jwt_token,
    test_db,
    sender_account_id,
    receiver_account_id,
    amount,
    expected_status_code,
):
    """
    In this test, we are testing the transfer of funds between two accounts.
    First we query the balance of the sender and receiver accounts before the transaction.
    Then we send a POST request to the /transactions/transfer/ endpoint to make a transfer.
    We check if the response status code and the details in the response are as expected.
    We also check if the balances of the sender and receiver accounts are updated correctly
    in the database.
    """

    sender_balance_before_transaction = test_db.execute(
        text(f"SELECT balance FROM accounts where id = {sender_account_id}")
    ).fetchone()[0]
    assert sender_balance_before_transaction is not None

    receiver_balance_before_transaction = test_db.execute(
        text(f"SELECT balance FROM accounts where id = {receiver_account_id}")
    ).fetchone()[0]
    assert receiver_balance_before_transaction is not None

    response = test_client.post(
        "/transactions/transfer/",
        json={
            "from_account": sender_account_id,
            "to_account": receiver_account_id,
            "amount": amount,
        },
        headers={"Authorization": f"Bearer {get_jwt_token}"},
    )
    assert response.status_code == expected_status_code
    assert response.json()["from_account"] == sender_account_id
    assert response.json()["to_account"] == receiver_account_id
    assert response.json()["amount"] == amount

    sender_account = test_db.execute(
        text(f"SELECT * FROM accounts where id = {sender_account_id}")
    ).fetchone()
    assert sender_account is not None
    assert sender_account[2] == sender_balance_before_transaction - amount
    assert sender_account[1] == sender_account_id

    receiver_account = test_db.execute(
        text(f"SELECT * FROM accounts where id = {receiver_account_id}")
    ).fetchone()
    assert receiver_account is not None
    assert receiver_account[2] == receiver_balance_before_transaction + amount
    assert receiver_account[1] == receiver_account_id


def test_get_transfer_history(
    test_client,
    get_jwt_token,
    test_db,
):
    """
    In this test, we are testing the retrieval of transfer history for a given account.
    First we transfert funds between two accounts.
    Then we send a GET request to the /transactions/history/{account_id} endpoint to get the
    transfer history.
    We check if the response status code and the details in the response are as expected.
    """

    sender_account_id = 1
    receiver_account_id = 2
    amount = 50

    response = test_client.post(
        "/transactions/transfer/",
        json={
            "from_account": sender_account_id,
            "to_account": receiver_account_id,
            "amount": amount,
        },
        headers={"Authorization": f"Bearer {get_jwt_token}"},
    )
    assert response.status_code == 200

    response = test_client.get(
        f"/transactions/history/{sender_account_id}",
        headers={"Authorization": f"Bearer {get_jwt_token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) != 0
    assert response.json()["history"][0]["from_account"] == sender_account_id
    assert response.json()["history"][0]["to_account"] == receiver_account_id
    assert response.json()["history"][0]["amount"] == amount
    assert response.json()["history"][0]["timestamp"] is not None


def test_transfter_more_than_balance(
    test_client,
    get_jwt_token,
    test_db,
):
    """
    In this test, we are testing the transfer of funds between two accounts, with an amount
    greater than the balance of the sender account.
    We expect an exception to be raised.
    """

    sender_account_id = 1
    receiver_account_id = 2
    amount = 1000000

    with pytest.raises(Exception):
        test_client.post(
            "/transactions/transfer/",
            json={
                "from_account": sender_account_id,
                "to_account": receiver_account_id,
                "amount": amount,
            },
            headers={"Authorization": f"Bearer {get_jwt_token}"},
        )
