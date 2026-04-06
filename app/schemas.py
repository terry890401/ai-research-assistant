from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str

class ResearchCreate(BaseModel):
    topic: str

class ResearchResponse(BaseModel):
    id: int
    user_id: int
    topic: str
    status: str
    result: str | None
    created_at: datetime

    class Config:
        from_attributes = True