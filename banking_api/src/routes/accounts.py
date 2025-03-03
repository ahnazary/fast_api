from banking_operations import create_account
from fastapi import APIRouter, Depends, HTTPException
from postgres_interface import get_db
from postgres_models import Account
from pydantic_models import AccountCreate, AccountResponse
from security import get_current_user
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create/", response_model=AccountResponse)
def create_new_account(
    account: AccountCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    new_account = create_account(db, account.customer_id, account.initial_deposit)
    return {"account_id": new_account.id, "balance": new_account.balance}


@router.get("/{account_id}/balance/", response_model=AccountResponse)
def get_balance(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_id": account.id, "balance": account.balance}
