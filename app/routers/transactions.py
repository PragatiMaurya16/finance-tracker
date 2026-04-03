from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date
from sqlalchemy import or_
from fastapi.responses import FileResponse

from app.database import SessionLocal
from app import crud, schemas, models
from app.utils import export_csv

router = APIRouter()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ROLE CHECK FUNCTION
def check_role(role: str, allowed_roles: list):
    if role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Access denied")


# GET with FILTERS + PAGINATION + SEARCH
@router.get("/", response_model=list[schemas.TransactionResponse])
def read_transactions(
    skip: int = 0,
    limit: int = 10,
    role: str = "viewer",
    type: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    check_role(role, ["viewer", "analyst", "admin"])

    query = db.query(models.Transaction)
    if search:
        query = query.filter(
            or_(
                models.Transaction.category.contains(search),
                models.Transaction.notes.contains(search)
            )
        )
    if type:
        query = query.filter(models.Transaction.type == type)

    if category:
        query = query.filter(models.Transaction.category == category)

    if start_date:
        query = query.filter(models.Transaction.date >= start_date)

    if end_date:
        query = query.filter(models.Transaction.date <= end_date)

    return query.offset(skip).limit(limit).all()

# CREATE
@router.post("/", response_model=schemas.TransactionResponse)
def create_transaction(
    txn: schemas.TransactionCreate,
    role: str,
    db: Session = Depends(get_db)
):
    check_role(role, ["admin"])
    return crud.create_transaction(db, txn, user_id=1)

# UPDATE
@router.put("/{txn_id}", response_model=schemas.TransactionResponse)
def update_transaction(
    txn_id: int,
    txn: schemas.TransactionCreate,
    role: str,
    db: Session = Depends(get_db)
):
    check_role(role, ["admin"])

    updated = crud.update_transaction(db, txn_id, txn)
    if not updated:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return updated

# DELETE
@router.delete("/{txn_id}")
def delete_transaction(
    txn_id: int,
    role: str,
    db: Session = Depends(get_db)
):
    check_role(role, ["admin"])

    deleted = crud.delete_transaction(db, txn_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return {"message": "Transaction deleted successfully"}

# BULK INSERT
@router.post("/bulk", response_model=list[schemas.TransactionResponse])
def create_bulk_transactions(
    txns: List[schemas.TransactionCreate],
    role: str,
    db: Session = Depends(get_db)
):
    check_role(role, ["admin"])
    return crud.create_transactions_bulk(db, txns, user_id=1)

# EXPORT TO CSV
@router.get("/export")
def export_transactions(
    role: str,
    db: Session = Depends(get_db)
):
    check_role(role, ["admin", "analyst"])

    data = db.query(models.Transaction).all()
    file_path = export_csv(data)

    return FileResponse(file_path, media_type="text/csv", filename="transactions.csv")