from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Sale(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    client_id: str
    book_id: str
    bookstore_id: str
    amount: float = Field(..., ge=0)
    sale_date: datetime = Field(default_factory=datetime.now)
    
    class Config:
        from_attributes = True
        populate_by_name = True
