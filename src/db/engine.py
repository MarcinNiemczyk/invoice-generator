from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# engine = create_engine("postgresql+psycopg2://postgres:password@db/postgres", echo=True)
engine = create_engine("postgresql+psycopg2://postgres:password@127.0.0.1:5432/postgres", echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
