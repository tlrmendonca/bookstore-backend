from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Client(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    address: Optional[str] = Field(None, max_length=200)
    is_active: bool = True  # Allows soft deletion while preserving borrowing history
    
    class Config:
        from_attributes = True
        populate_by_name = True
