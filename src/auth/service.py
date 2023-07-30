from sqlalchemy.orm import Session

from src.auth.model import User
from src.auth.schemas import UserRegister
from src.config import pwd_context


def get_password_hash(*, password: str) -> str:
    return pwd_context.hash(password)


def create_new_user(*, db_session: Session, user_in: UserRegister) -> None:
    hashed_password = get_password_hash(password=user_in.password)
    user = User(
        email=user_in.email,
        password=hashed_password
    )
    db_session.add(user)
    db_session.commit()


def get_all_users(*, db_session: Session) -> list[User] | list:
    return db_session.query(User).all()


def get_user_by_email(*, db_session: Session, email: str) -> User | None:
    return db_session.query(User).filter(User.email == email).one_or_none()
