"""
Pydantic models for request and response bodies.
Requests sent to the API are validated using these models.
"""

from datetime import datetime

from pydantic import BaseModel


class AccountCreate(BaseModel):
    customer_id: int
    initial_deposit: float


class TransferRequest(BaseModel):
    from_account: int
    to_account: int
    amount: float


class AccountResponse(BaseModel):
    account_id: int
    balance: float


class TransactionResponse(BaseModel):
    from_account: int
    to_account: int
    amount: float
    timestamp: datetime


class CustomerCreate(BaseModel):
    id: int
    name: str


class UsersCreate(BaseModel):
    username: str
    password: str
