from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from backend.db.engine import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
