from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User
