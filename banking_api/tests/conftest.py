"""
Module to define fixtures for the tests.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.postgres_interface import (
    SessionLocal,
    create_tables,
    fill_tables,
    reset_tables,
)


@pytest.fixture(scope="function")
def test_db():
    """
    This fixture will create a new session for the tests.
    it will reset the tables after each test.
    """
    yield SessionLocal()
    reset_tables()
    SessionLocal().close()


@pytest.fixture(scope="module")
def test_client():
    """
    This fixture will create a test client for the FastAPI application.
    """
    create_tables()
    fill_tables()
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def get_jwt_token():
    """
    This fixture will return a JWT token for the tests.
    The bearer token is generated using the admin credentials.
    """
    response = TestClient(app).post(
        "/auth/token", data={"username": "admin", "password": "admin123"}
    )
    return response.json()["access_token"]
