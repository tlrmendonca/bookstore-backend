from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Any
import os

# MongoDB connection
print(f"MongoDB URL: {os.getenv('MONGODB_URL', 'NOT SET')}")
mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client : AsyncIOMotorClient[Any] = AsyncIOMotorClient(
    mongo_url,
    serverSelectionTimeoutMS=5000,
    socketTimeoutMS=10000
)
db : AsyncIOMotorDatabase = client.bookstore