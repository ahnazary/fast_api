"""Module for defining the postgres database models"""

from datetime import datetime

from postgres_interface import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Customer(Base):
    """
    Model for the customers table
    """

    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Account(Base):
    """
    Model for the accounts table
    we assume that the customer_id is a foreign key to the customers table
    """

    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    balance = Column(Float, default=0.0)

    customer = relationship("Customer")


class Transaction(Base):
    """
    Model for the transactions table
    we assume that the from_account and to_account are foreign keys to the accounts
    """

    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    from_account = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    to_account = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
