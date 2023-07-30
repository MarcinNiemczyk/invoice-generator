from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from sqlalchemy.orm import Mapped, mapped_column

from src.db.engine import Base
from src.config import pwd_context, config


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=config.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
        data = {
            "exp": exp,
            "email": self.email,
        }
        return jwt.encode(data, config.SECRET_KEY, algorithm=config.ALGORITHM)

    def check_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)
