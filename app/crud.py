from sqlalchemy.orm import Session
from app import models, schemas


# CREATE TRANSACTION
def create_transaction(db: Session, txn: schemas.TransactionCreate, user_id: int):
    new_txn = models.Transaction(
        amount=txn.amount,
        type=txn.type,
        category=txn.category,
        date=txn.date,
        notes=txn.notes,
        user_id=user_id
    )
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return new_txn


# GET ALL TRANSACTIONS
def get_transactions(db: Session):
    return db.query(models.Transaction).all()


# GET SINGLE TRANSACTION
def get_transaction(db: Session, txn_id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == txn_id).first()


# UPDATE TRANSACTION
def update_transaction(db: Session, txn_id: int, txn: schemas.TransactionCreate):
    existing_txn = db.query(models.Transaction).filter(models.Transaction.id == txn_id).first()
    
    if not existing_txn:
        return None

    existing_txn.amount = txn.amount
    existing_txn.type = txn.type
    existing_txn.category = txn.category
    existing_txn.date = txn.date
    existing_txn.notes = txn.notes

    db.commit()
    db.refresh(existing_txn)
    return existing_txn


# DELETE TRANSACTION
def delete_transaction(db: Session, txn_id: int):
    txn = db.query(models.Transaction).filter(models.Transaction.id == txn_id).first()
    
    if not txn:
        return None

    db.delete(txn)
    db.commit()
    return txn

# BULK INSERT
def create_transactions_bulk(db: Session, txns: list[schemas.TransactionCreate], user_id: int):
    new_txns = []

    for txn in txns:
        new_txn = models.Transaction(
            amount=txn.amount,
            type=txn.type,
            category=txn.category,
            date=txn.date,
            notes=txn.notes,
            user_id=user_id
        )
        new_txns.append(new_txn)

    db.add_all(new_txns)
    db.commit()

    return new_txns