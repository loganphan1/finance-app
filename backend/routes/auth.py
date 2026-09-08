from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend import models
from backend.schema import UserCreate, UserResponse, TokenResponse
from backend.database import get_db
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from typing import Optional

router = APIRouter()
token_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login")

load_dotenv()  # Load environment variables from .env file
secret_key = os.getenv("secret_key")
algorithm = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

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

@router.post("/auth/login", response_model = TokenResponse)

async def login_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(token_oauth2),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = jwt.decode(token,secret_key, algorithms=[algorithm])
        email: str = decoded_token.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user