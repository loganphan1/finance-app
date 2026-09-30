from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    merchant: str
    category: str
    date: date

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "amount": "100.00",
                "merchant": "Amazon",
                "category": "Shopping",
                "date": "2024-01-01"
            }
        }
    )

class TransactionResponse(BaseModel):
    id: int
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    merchant: str
    category: str
    date: date

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "amount": "100.00",
                "merchant": "Amazon",
                "category": "Shopping",
                "date": "2024-01-01"
            }
        }
    )

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "password": "securepassword"
            }
        }
    )


class UserLogin(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "john.doe@example.com",
                "password": "securepassword",
            }
        }
    )


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john.doe@example.com"
            }
        }
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "your_access_token",
                "token_type": "bearer"
            }
        }
    )
