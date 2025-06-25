from fastapi import APIRouter, HTTPException, status
from ..models.client import Client
from bson import ObjectId
from bson.errors import InvalidId

from ..db import db
from ..utils.utils import *

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_client(client: Client) -> Client:
    """Create a new client in the database"""
    client_dict = client.model_dump(by_alias=True, exclude_none=True)
    client_dict.pop("_id", None)

    result = await db.clients.insert_one(client_dict)
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to create client")
    
    client_dict["_id"] = str(result.inserted_id)
    return Client(**client_dict)


@router.get("/{client_id}")
async def get_client(client_id: str) -> Client:
    """Get a single client by its MongoDB ObjectId"""
    client_object_id = validate_object_id(client_id, "client")
   
    client_data = await db.clients.find_one({"_id": client_object_id})
    if not client_data:
        raise HTTPException(status_code=404, detail="Client not found")
   
    client_data["_id"] = str(client_data["_id"])
    return Client(**client_data)


@router.put("/{client_id}")
async def update_client(client_id: str, client: Client) -> Client:
    """Update a client by its MongoDB ObjectId"""
    client_object_id = validate_object_id(client_id, "client")
    
    client_dict = client.model_dump(by_alias=True, exclude_none=True)
    client_dict.pop("_id", None)

    result = await db.clients.update_one({"_id": client_object_id}, {"$set": client_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Client not found")

    updated_client = await db.clients.find_one({"_id": client_object_id})
    if not updated_client:
        raise HTTPException(status_code=404, detail="Client not found after update")
    updated_client["_id"] = str(updated_client["_id"])
    return Client(**updated_client)


@router.delete("/{client_id}")
async def delete_client(client_id: str) -> None:
    """Delete a client by its MongoDB ObjectId"""
    client_object_id = validate_object_id(client_id, "client")
   
    result = await db.clients.delete_one({"_id": client_object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return

