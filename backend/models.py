from sqlalchemy import Column, Integer, String, Float,Date
from backend.database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    merchant = Column(String, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class TokenResponse(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, nullable=False)
    token_type = Column(String, nullable=False)