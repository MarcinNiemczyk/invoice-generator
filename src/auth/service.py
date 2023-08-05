from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.auth.model import User
from src.auth.schemas import UserRegister
from src.config import config, pwd_context
from src.db.engine import get_db


def get_password_hash(*, password: str) -> str:
    return pwd_context.hash(password)


def get_all_users(*, db_session: Session) -> list[User] | list:
    return db_session.query(User).all()


def get_user_by_email(*, db_session: Session, email: str) -> User | None:
    return db_session.query(User).filter(User.email == email).one_or_none()


def validate_email(*, db_session: Session, email: str) -> None:
    if get_user_by_email(db_session=db_session, email=email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )


def create_new_user(*, db_session: Session, user_in: UserRegister) -> None:
    validate_email(db_session=db_session, email=user_in.email)
    hashed_password = get_password_hash(password=user_in.password)
    user = User(email=user_in.email, password=hashed_password)
    db_session.add(user)
    db_session.commit()


def verify_token(*, x_token: Annotated[str, Header()]):
    try:
        jwt.decode(x_token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="X-Token header invalid"
        )


def decode_token(*, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="X-Token header invalid"
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
    except JWTError:
        raise credentials_exception

    email = payload.get("email")
    if email is None:
        raise credentials_exception

    return email


def get_current_user(
    *, x_token: Annotated[str, Header()], db_session: Session = Depends(get_db)
) -> User | None:
    email = decode_token(token=x_token)
    return get_user_by_email(db_session=db_session, email=email)
