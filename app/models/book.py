from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class BookCondition(str, Enum):
    NEW = "New"
    GOOD = "Good"
    POOR = "Poor"
    VERY_POOR = "Very Poor"


class Book(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    isbn: str = Field(..., min_length=10, max_length=13)
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    genre: Optional[str] = None
    price: float = Field(..., ge=0)
    condition: BookCondition = BookCondition.NEW
    
    class Config:
        from_attributes = True
        populate_by_name = True