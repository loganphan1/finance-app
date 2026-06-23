from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schema import TransactionCreate, TransactionResponse
from backend import models
router = APIRouter()

@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
        new_transaction = models.Transaction(
            amount=transaction.amount,
            merchant=transaction.merchant,
            category=transaction.category,
            date=transaction.date
        )
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        return new_transaction

@router.get("/transactions", response_model=list[TransactionResponse])
async def get_transactions(db: Session = Depends(get_db)):
        return db.query(models.Transaction).all()

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
        transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction