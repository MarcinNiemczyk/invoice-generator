from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.auth.model import User
from src.auth.schemas import Token, UserLogin, UserRead, UserRegister
from src.auth.service import (
    create_new_user,
    get_all_users,
    get_current_user,
    get_user_by_email,
    verify_token,
)
from src.db.engine import get_db

auth_router = APIRouter()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db_session: Session = Depends(get_db)):
    create_new_user(db_session=db_session, user_in=user_in)


@auth_router.post("/login", response_model=Token)
def login(user_in: UserLogin, db_session: Session = Depends(get_db)):
    user = get_user_by_email(db_session=db_session, email=user_in.email)
    if not user or not user.check_password(user_in.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return {"access_token": user.token}


@auth_router.get("/users", response_model=list[UserRead])
def list_users(db_session: Session = Depends(get_db)):
    return get_all_users(db_session=db_session)


@auth_router.get("/users/access", dependencies=[Depends(verify_token)])
def check_token():
    return {"access": "granted"}


@auth_router.get("/users/me", response_model=UserRead)
def read_current_user(user: Annotated[User, Depends(get_current_user)]):
    return user
