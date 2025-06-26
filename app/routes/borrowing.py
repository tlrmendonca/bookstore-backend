from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models.borrowing import Borrowing, SourceType

from ..db import db
from ..services.borrowing import *
from ..utils.utils import validate_object_id

router = APIRouter(prefix="/borrowings", tags=["borrowings"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_borrowing(borrowing: Borrowing) -> Borrowing:
    """Create a new borrowing in the database"""
    borrowing_dict = borrowing.model_dump(by_alias=True, exclude_none=True)
    borrowing_dict.pop("_id", None)

    result = await db.borrowings.insert_one(borrowing_dict)
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to create borrowing")

    borrowing_dict["_id"] = str(result.inserted_id)
    return Borrowing(**borrowing_dict)


@router.get("/{borrowing_id}")
async def get_borrowing(borrowing_id: str) -> Borrowing:
    """Get a single borrowing by its MongoDB ObjectId"""
    borrowing_object_id = validate_object_id(borrowing_id, "borrowing")

    borrowing_data = await db.borrowings.find_one({"_id": borrowing_object_id})
    if not borrowing_data:
        raise HTTPException(status_code=404, detail="Borrowing not found")

    borrowing_data["_id"] = str(borrowing_data["_id"])
    return Borrowing(**borrowing_data)

@router.get("/")
async def get_borrowings() -> List[Borrowing]:
    """Get all borrowings in the database"""
    borrowings_data = await db.borrowings.find().to_list(length=None)
    if not borrowings_data:
        raise HTTPException(status_code=404, detail="No borrowings found")

    for borrowing in borrowings_data:
        borrowing["_id"] = str(borrowing["_id"])

    return [Borrowing(**borrowing) for borrowing in borrowings_data]

@router.get("/client/{client_id}")
async def get_borrowings_by_client(client_id: str) -> List[Borrowing]:
    """Get all borrowings for a specific client by their MongoDB ObjectId"""
    client_object_id = validate_object_id(client_id, "client")

    borrowings_data = await db.borrowings.find({
        "borrower_id": str(client_object_id),
        "source_type": SourceType.CLIENT
    }).to_list(length=None)
    if not borrowings_data:
        raise HTTPException(status_code=404, detail="No borrowings found for this client")

    for borrowing in borrowings_data:
        borrowing["_id"] = str(borrowing["_id"])

    return [Borrowing(**borrowing) for borrowing in borrowings_data]


@router.get("/bookstore/{bookstore_id}")
async def get_borrowings_by_bookstore(bookstore_id: str) -> List[Borrowing]:
    """Get all borrowings from a specific bookstore by its MongoDB ObjectId"""
    bookstore_object_id = validate_object_id(bookstore_id, "bookstore")

    borrowings_data = await db.borrowings.find({
        "source_id": str(bookstore_object_id),
        "source_type": SourceType.BOOKSTORE
    }).to_list(length=None)
    if not borrowings_data:
        raise HTTPException(status_code=404, detail="No borrowings found for this bookstore")

    for borrowing in borrowings_data:
        borrowing["_id"] = str(borrowing["_id"])

    return [Borrowing(**borrowing) for borrowing in borrowings_data]

@router.get("return/{borrowing_id}")
async def return_borrowing(borrowing_id: str) -> Borrowing:
    """Mark a borrowing as returned by its MongoDB ObjectId"""
    borrowing_object_id = validate_object_id(borrowing_id, "borrowing")

    return await process_borrowing_return(borrowing_id=borrowing_object_id)
    