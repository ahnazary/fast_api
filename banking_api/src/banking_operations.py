from postgres_models import Account, Customer, Transaction
from pydantic_models import TransferRequest
from sqlalchemy.orm import Session


def create_account(db: Session, customer_id: int, initial_deposit: float):
    """
    Function that is used for creating account based on the customer_id and initial_deposit

    args
    ----
    db: Session
        The database session
    customer_id: int
        The customer id
    initial_deposit: float
        The initial deposit amount

    returns
    -------
    Account
        The account object
    """
    new_account = Account(customer_id=customer_id, balance=initial_deposit)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


def transfer_money(db: Session, transfer: TransferRequest):
    """
    Function that is used for transferring money between two accounts.
    Here we choose the first query result as the sender and receiver accounts.

    args
    ----
    db: Session
        The database session
    transfer: TransferRequest
        The transfer request object

    returns
    -------
    Transaction
        The transaction object
    """
    sender = db.query(Account).filter(Account.id == transfer.from_account).first()
    receiver = db.query(Account).filter(Account.id == transfer.to_account).first()

    if not sender or not receiver:
        return {"error": "Account not found, please check the account numbers"}

    if sender.balance < transfer.amount:
        return {"error": "Insufficient funds, please check the balance"}

    sender.balance -= transfer.amount
    receiver.balance += transfer.amount
    transaction = Transaction(
        from_account=sender.id, to_account=receiver.id, amount=transfer.amount
    )
    db.add(transaction)
    db.commit()
    return transaction


def create_customer(db: Session, customer_id: int, name: str):
    """
    Function that is used for creating customer based on the customer_id and name

    args
    ----
    db: Session
        The database session
    customer_id: int
        The customer id
    name: str
        The customer name

    returns
    -------
    Customer
        The customer object
    """
    new_customer = Customer(id=customer_id, name=name)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def get_transfer_history(db: Session, account_id: int):
    """
    Function that is used for getting the transfer history for a given account

    args
    ----
    db: Session
        The database session
    account_id: int
        The account id

    returns
    -------
    List[Transaction]
        The list of transaction objects
    """
    return (
        db.query(Transaction)
        .filter(
            (Transaction.from_account == account_id)
            | (Transaction.to_account == account_id)
        )
        .all()
    )
