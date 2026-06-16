from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from datetime import date
app = FastAPI()

class Transaction(BaseModel):
    id: int
    amount: float
    merchant: str
    category: str
    date: date
    
    model_config = ConfigDict(
        schema_extra={
            "example": {
                "id": 1,
                "amount": 100.0,
                "merchant": "Amazon",
                "category": "Shopping",
                "date": "2024-01-01"
            }
        }
    )
