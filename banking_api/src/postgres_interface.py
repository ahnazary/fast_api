"""
Module for interacting with the postgres database
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# The default value for the DATABASE_URL is set in docker-compose.yml file.
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5433/banking"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Function that creates the tables in the database if they don't exist.
    These serve as the backend for the API.
    """
    with engine.connect() as conn:
        conn.execute(
            text(
                """
            -- Create the customers table
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );

            -- Create the accounts table
            CREATE TABLE IF NOT EXISTS accounts (
                id SERIAL PRIMARY KEY,
                customer_id INT NOT NULL,
                balance NUMERIC(15, 2) DEFAULT 0.00,
                FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
            );

            -- Create the transactions table
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                from_account INT NOT NULL,
                to_account INT NOT NULL,
                amount NUMERIC(15, 2) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_account) REFERENCES accounts(id) ON DELETE CASCADE,
                FOREIGN KEY (to_account) REFERENCES accounts(id) ON DELETE CASCADE
            );
        """
            )
        )
        conn.commit()


def fill_tables():
    """
    Function that fills the tables with some initial data mentioned in the task.
    """
    with engine.connect() as conn:
        conn.execute(
            text(
                """
            -- Insert some initial data based on the task requirements
            INSERT INTO customers (id, name) VALUES
            (1, 'Arisha Barron'),
            (2, 'Branden Gibson'),
            (3, 'Rhonda Church'),
            (4, 'Georgina Hazel')
            on conflict do
            nothing;

            -- Insert accounts with initial deposits
            INSERT INTO accounts (customer_id, balance) VALUES
            (1, 1000.00),
            (2, 1500.00),
            (3, 2000.00),
            (4, 2500.00)
            on conflict do
            nothing;
        """
            )
        )
        conn.commit()


def reset_tables():
    """
    Function that sets the tables to their initial state.
    This is going to be used in the tests to clean the tables before running the tests.
    """
    with engine.connect() as conn:
        conn.execute(
            text(
                """
            -- Delete all the data from the tables
            DELETE FROM transactions;
            DELETE FROM accounts;
            DELETE FROM customers;

            -- Reset the sequences
            ALTER SEQUENCE transactions_id_seq RESTART WITH 1;
            ALTER SEQUENCE accounts_id_seq RESTART WITH 1;
            ALTER SEQUENCE customers_id_seq RESTART WITH 1;
            """
            )
        )
        conn.commit()
        # Re-insert the initial data
        fill_tables()
