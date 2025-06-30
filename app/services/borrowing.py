from fastapi import HTTPException
from ..models.borrowing import Borrowing, BorrowingStatus
from datetime import datetime
import logging
from bson import ObjectId

from ..db import db

async def process_borrowing_return(borrowing_id : ObjectId) -> Borrowing:
    """Mark a borrowing as returned by its MongoDB ObjectId"""
    now = datetime.now()

    borrowing_data = await db.borrowings.find_one({'_id': borrowing_id})
    print(f"Found borrowing data: {borrowing_data}")
    if not borrowing_data:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    

    borrowing_data["_id"] = str(borrowing_data["_id"])
    borrowing_data["source_id"] = str(borrowing_data["source_id"])
    borrowing_data["borrower_id"] = str(borrowing_data["borrower_id"])
    borrowing_data["book_id"] = str(borrowing_data["book_id"])
    borrowing = Borrowing(**borrowing_data)
    overdue : bool = now > borrowing.due_date

    result = await db.borrowings.update_one(
        {"_id": borrowing_id},
        {"$set": {"return_date": now, "status": BorrowingStatus.RETURNED_OVERDUE if overdue else BorrowingStatus.RETURNED}},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Borrowing already returned")
    
    if overdue:
        apply_overdue_fee(borrowing.borrower_id, borrowing)
    
    borrowing.return_date = now
    borrowing.status = BorrowingStatus.RETURNED_OVERDUE if overdue else BorrowingStatus.RETURNED
    return borrowing
        
def apply_overdue_fee(borrower_id: str, borrowing: Borrowing) -> None:
    """Apply an overdue fee to the borrower if the borrowing is overdue"""
    logging.warning(f"TODO: Apply overdue fee to borrower {borrower_id}")
    logging.warning(f"Due date: {borrowing.due_date}; Return date: {borrowing.return_date}")
    pass