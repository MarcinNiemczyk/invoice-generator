from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserBase(BaseModel):
    first_name: Optional[str] = Field(..., max_length=50)
    last_name: Optional[str] = Field(..., max_length=50)
    email: EmailStr


class User(UserBase):
    pass


class UserCreate(UserBase):
    password: str
