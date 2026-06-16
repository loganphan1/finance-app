from fastapi import FastAPI
from routes.schema import Transaction
app = FastAPI()

@app.post("/transactions", response_model=list[Transaction])
async def create_transaction(transaction: Transaction):
    return [
        Transaction(
            id=1,
            amount="25.50",
            merchant="Starbucks",
            category="Food & Drink",
            date="2024-01-15"
        ),
        Transaction(
            id=2,
            amount="100.00",
            merchant="Amazon",
            category="Shopping",
            date="2024-01-10"
        )
    ]