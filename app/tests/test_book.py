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
async def test_get_books(test_db):
    """Test the GET /books endpoint."""
    # populate db
    await populate_db()

    response = client.get("/books/?limit=100")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    await clear_db()
