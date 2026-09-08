from fastapi import Depends, APIRouter, HTTPException
from backend.routes.auth import get_current_user
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schema import TransactionCreate, TransactionResponse
from backend import models
router = APIRouter()

@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
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
async def get_transactions(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
        return db.query(models.Transaction).all()

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
        transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction

@router.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
        transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        db.delete(transaction)
        db.commit()
        return {"message": "Transaction deleted successfully"}