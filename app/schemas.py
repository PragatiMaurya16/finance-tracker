from pydantic import BaseModel
from datetime import date

class TransactionCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: date
    notes: str | None = None


class TransactionResponse(TransactionCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True