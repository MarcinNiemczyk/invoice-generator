from typing import Optional

from pydantic import BaseModel, EmailStr, Field  # noqa: F401


class UserCreate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: str


class UserRead(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: str
