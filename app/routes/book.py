from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models.book import Book
from bson import ObjectId
from bson.errors import InvalidId

from ..db import db
from ..utils.utils import *

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book) -> Book:
    """Create a new book in the database"""
    book_dict = book.model_dump(by_alias=True, exclude_none=True)
    book_dict.pop("_id", None)

    result = await db.books.insert_one(book_dict)
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to create book")

    book_dict["_id"] = str(result.inserted_id)
    return Book(**book_dict)


@router.get("/{book_id}")
async def get_book(book_id: str) -> Book:
    """Get a single book by its MongoDB ObjectId"""
    book_object_id = validate_object_id(book_id, "book")
    
    book_data = await db.books.find_one({"_id": book_object_id})
    if not book_data:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_data["_id"] = str(book_data["_id"])
    return Book(**book_data)

@router.get("/")
async def get_books() -> List[Book]:
    """Get all books in the database"""
    books_data = await db.books.find().to_list(length=None)
    if not books_data:
        raise HTTPException(status_code=404, detail="No books found")

    for book in books_data:
        book["_id"] = str(book["_id"])

    return [Book(**book) for book in books_data]

@router.delete("/{book_id}")
async def delete_book(book_id: str) -> None:
    """Delete a book by its MongoDB ObjectId"""
    book_object_id = validate_object_id(book_id, "book")

    
    result = await db.books.delete_one({"_id": book_object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")

    return