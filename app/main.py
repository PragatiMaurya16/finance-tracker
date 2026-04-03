from fastapi import FastAPI
from app.database import Base, engine
from app import models 
from app.routers import transactions
from app.routers import analytics

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(transactions.router)
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])  
