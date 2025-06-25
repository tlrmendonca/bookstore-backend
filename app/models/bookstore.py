from pydantic import BaseModel, Field
from typing import Optional


class BookInventory(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    bookstore_id: str
    isbn: int
    quantity_available: int = Field(..., ge=0)
    
    class Config:
        from_attributes = True
        populate_by_name = True



class Bookstore(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str = Field(..., min_length=1, max_length=100)
    address: str = Field(..., min_length=1, max_length=200)
    email: Optional[str] = None
    
    class Config:
        from_attributes = True
        populate_by_name = True
