from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Transaction
from sqlalchemy import extract, func
from app.models import Transaction

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    total_income = db.query(func.sum(Transaction.amount)).filter(Transaction.type == "income").scalar() or 0

    total_expense = db.query(func.sum(Transaction.amount)).filter(Transaction.type == "expense").scalar() or 0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }

@router.get("/monthly")
def monthly_summary(db: Session = Depends(get_db)):
    data = db.query(
        extract('month', Transaction.date).label("month"),
        func.sum(Transaction.amount).label("total")
    ).group_by("month").all()

    return [
        {"month": int(month), "total": total}
        for month, total in data
    ]