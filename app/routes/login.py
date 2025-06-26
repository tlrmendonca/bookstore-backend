from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Simple login endpoint - accepts a hardcoded password."""
    if request.password != "password":
        raise HTTPException(status_code=401, detail="Invalid password")
    
    token_data = {
        "sub": "demo_user",
        "authenticated": True
    }
    
    access_token = create_access_token(token_data)
    
    return TokenResponse(access_token=access_token)