from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models.bookstore import Bookstore, BookInventory
from bson import ObjectId
from bson.errors import InvalidId

from ..db import db
from ..utils.utils import validate_object_id

router = APIRouter(prefix="/bookstores", tags=["bookstores"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_bookstore(bookstore: Bookstore) -> Bookstore:
    """Create a new bookstore in the database"""
    bookstore_dict = bookstore.model_dump(by_alias=True, exclude_none=True)
    bookstore_dict.pop("_id", None)

    result = await db.bookstores.insert_one(bookstore_dict)
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to create bookstore")

    bookstore_dict["_id"] = str(result.inserted_id)
    return Bookstore(**bookstore_dict)


@router.get("/{bookstore_id}")
async def get_bookstore(bookstore_id: str) -> Bookstore:
    """Get a single bookstore by its MongoDB ObjectId"""
    bookstore_object_id = validate_object_id(bookstore_id, "bookstore")

    bookstore_data = await db.bookstores.find_one({"_id": bookstore_object_id})
    if not bookstore_data:
        raise HTTPException(status_code=404, detail="Bookstore not found")

    bookstore_data["_id"] = str(bookstore_data["_id"])
    return Bookstore(**bookstore_data)


@router.post("/{bookstore_id}/inventory", status_code=status.HTTP_201_CREATED)
async def add_book_inventory(bookstore_id: str, inventory: BookInventory) -> BookInventory:
    """Add a book inventory to a bookstore"""
    validate_object_id(bookstore_id, "bookstore")

    inventory_dict = inventory.model_dump(by_alias=True, exclude_none=True)
    inventory_dict.pop("_id", None)

    result = await db.book_inventories.insert_one(inventory_dict)
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to add book inventory")
    
    inventory_dict["_id"] = str(result.inserted_id)
    return BookInventory(**inventory_dict)


@router.get("/{bookstore_id}/inventory")
async def get_bookstore_inventory(bookstore_id: str) -> List[BookInventory]:
    """Get all book inventories for a specific bookstore by its MongoDB ObjectId"""
    validate_object_id(bookstore_id, "bookstore")

    inventories_data = await db.book_inventories.find({"bookstore_id": bookstore_id}).to_list(length=None)
    if not inventories_data:
        raise HTTPException(status_code=404, detail="No inventories found for this bookstore")

    for inventory in inventories_data:
        inventory["_id"] = str(inventory["_id"])

    return [BookInventory(**inventory) for inventory in inventories_data]