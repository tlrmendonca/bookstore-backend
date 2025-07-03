from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Any
import pytest, pytest_asyncio

from .. import db as db_module

from ..main import app
from .utils import *

@pytest_asyncio.fixture
async def setup_test_db():
    """Create and setup test database."""
    client: AsyncIOMotorClient[Any] = AsyncIOMotorClient(
        "mongodb://localhost:27018",
        serverSelectionTimeoutMS=5000
    )
    test_db = client.bookstore
    
    # Set the test database
    original_db = db_module.db
    db_module.db = test_db
    
    # Populate database
    await populate_db()
    
    yield test_db
    
    # Cleanup
    db_module.db = original_db
    client.close()

client = TestClient(app=app)

@pytest.mark.asyncio
async def test_get_borrowings():
    """Test the GET /books endpoint."""

    response = client.get("/borrowings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_return_borrowing():
    """Test the POST /borrowings/return/{borrowing_id} endpoint."""

    # Get a borrowing to return
    borrowings_response = client.get("/borrowings/")
    assert borrowings_response.status_code == 200

    borrowings = borrowings_response.json()
    
    return_response = client.post(f"/borrowings/return/{borrowings[0]['_id']}")
    print(return_response.json())
    assert return_response.status_code == 200
    assert return_response.json().get("status") in ("returned", "returned_overdue") 
    
    
