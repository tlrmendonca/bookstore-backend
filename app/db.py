from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Any

# MongoDB connection
client : AsyncIOMotorClient[Any] = AsyncIOMotorClient(
    "mongodb://localhost:27017",
    serverSelectionTimeoutMS=5000
    )
db : AsyncIOMotorDatabase = client.bookstore