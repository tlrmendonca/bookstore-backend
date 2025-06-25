from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class BorrowingStatus(str, Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"
    RETURNED_OVERDUE = "returned_overdue"


class SourceType(str, Enum):
    BOOKSTORE = "bookstore"
    CLIENT = "client"


class Borrowing(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    borrower_id: str  # client who borrowed
    source_type: SourceType  # More robust than separate lender_id/bookstore_id fields
    source_id: str  # ID of bookstore or client providing the book
    book_id: str
    borrow_date: datetime = Field(default_factory=datetime.now)
    due_date: datetime
    return_date: Optional[datetime] = None
    status: BorrowingStatus = BorrowingStatus.ACTIVE
    
    class Config:
        from_attributes = True
        populate_by_name = True
