from banking_operations import create_customer
from fastapi import APIRouter, Depends
from postgres_interface import get_db
from pydantic_models import CustomerCreate
from security import get_current_user
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create/", response_model=CustomerCreate)
def create_new_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    new_customer = create_customer(db, customer.id, customer.name)
    return new_customer
