from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.auth import schema, model
from backend.db.engine import get_db


router = APIRouter()


@router.post("/users/", status_code=201)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = model.User(
        email=user.email,
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


@router.get("/users/", response_model=list[schema.UserRead])
def read_users(db: Session = Depends(get_db)):
    users = db.query(model.User).all()
    return users
