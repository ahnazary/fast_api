from banking_operations import get_transfer_history, transfer_money
from fastapi import APIRouter, Depends, HTTPException
from postgres_interface import get_db
from postgres_models import Transaction
from pydantic_models import TransactionResponse, TransferRequest
from security import get_current_user
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/transfer/", response_model=TransactionResponse)
def transfer_funds(
    transfer: TransferRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
) -> Transaction:
    """
    This endpoint is used for transferring funds between two accounts.
    The transfer request object is passed as a parameter to this endpoint.

    args
    ----
    transfer: TransferRequest
        The transfer request object

    returns
    -------
    Transaction
        The transaction
    """
    transaction = transfer_money(db, transfer)
    if not transaction:
        raise HTTPException(
            status_code=400, detail="An error occurred while processing the transaction"
        )
    return transaction


@router.get("/history/{account_id}", response_model=dict)
def transfer_history(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """
    This endpoint is used for getting the transfer history for a given account.

    args
    ----
    account_id: int
        The account id for which the transfer history needs to be retrieved

    returns
    -------
    List[Transaction]
        The list of transactions for the given account
    """
    history = get_transfer_history(db, account_id)
    result = []
    for transaction in history:
        result.append(
            {
                "from_account": transaction.from_account,
                "to_account": transaction.to_account,
                "amount": transaction.amount,
                "timestamp": transaction.timestamp,
            }
        )
    return {"history": result}
