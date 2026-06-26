from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend import models
from backend.schema import UserCreate, UserResponse
from backend.database import get_db

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/auth/register", response_model = UserResponse)

async def register_user(user:UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user