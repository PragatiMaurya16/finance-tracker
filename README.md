# Finance Tracker API

## Overview
A backend system to manage financial transactions with analytics and role-based design.

## Features
- CRUD for transactions
- Pagination support
- Financial summary (income, expense, balance)
- Basic user roles

## Tech Stack
- FastAPI
- SQLite
- SQLAlchemy

## Run Locally

pip install -r requirements.txt

## Steps to run the Project
1. Clone the repository
2. Create virtual environment
3. Install requirements
4. Run server using uvicorn
5. Open http://127.0.0.1:8000/docs
uvicorn app.main:app --reload

## API Docs
http://127.0.0.1:8000/docs

## Example Endpoints

POST /transactions
GET /transactions
DELETE /transactions/{id}
GET /analytics/summary
