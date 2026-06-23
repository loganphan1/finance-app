from pydantic import BaseModel, ConfigDict
from datetime import date

class TransactionCreate(BaseModel):
    amount: float
    merchant: str
    category: str
    date: date
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "amount": 100.0,
                "merchant": "Amazon",
                "category": "Shopping",
                "date": "2024-01-01"
            }
        }
    )

class TransactionResponse(BaseModel):
    id: int
    amount: float
    merchant: str
    category: str
    date: date
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "amount": 100.0,
                "merchant": "Amazon",
                "category": "Shopping",
                "date": "2024-01-01"
            }
        }
    )
