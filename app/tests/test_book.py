import pytest
import httpx

from .db import db as test_db
from .. import db as db_module
# Select the test database
db_module.db = test_db

from ..main import app
from .utils import *

client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")

def pytest_runtest_module_teardown():
    import asyncio
    asyncio.run(client.aclose())

@pytest.mark.asyncio
async def test_get_books():
    """Test the GET /books endpoint."""
    # populate db
    await populate_db()

    response = await client.get("/books/?limit=100")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

    await clear_db()
