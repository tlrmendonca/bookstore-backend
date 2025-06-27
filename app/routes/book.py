from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from ..models.book import Book

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
async def get_books(limit: int = Query(20, le=100), cursor: Optional[str] = None) -> dict:
    """Get all books in the database"""
    print(f"Fetching books with cursor: {cursor} and limit: {limit}")
    query = {}
    # cursor is the object Id in string format that bookmarks the last fetched book
    if cursor:
        query["_id"] = {"$gt": ObjectId(cursor)}

    books_data = await db.books.find(query).sort("_id", 1).limit(limit).to_list(limit)
    if not books_data:
        raise HTTPException(status_code=404, detail="No books found")
    
    for book in books_data:
        book["_id"] = str(book["_id"])

    # prepare return
    books = [Book(**book) for book in books_data]
    next_cursor = str(books_data[-1]["_id"])

    return {
        "books": books,
        "next_cursor": next_cursor,
        "has_more": len(books_data) == limit
    }

@router.delete("/{book_id}")
async def delete_book(book_id: str) -> None:
    """Delete a book by its MongoDB ObjectId"""
    book_object_id = validate_object_id(book_id, "book")

    
    result = await db.books.delete_one({"_id": book_object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")

    return