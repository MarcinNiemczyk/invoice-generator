from typing import Optional

from pydantic import BaseModel, EmailStr, Field  # noqa: F401


class UserRegister(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr


class Token(BaseModel):
    access_token: str
