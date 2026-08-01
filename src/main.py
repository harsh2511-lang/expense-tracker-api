from fastapi import FastAPI, HTTPException
from typing import Optional
from src.models import Expense, ExpenseCreate
from src.storage import store

app = FastAPI(title="Smart Expense Tracker API")


@app.post("/expenses", response_model=Expense, status_code=201)
def add_expense(expense: ExpenseCreate):
    return store.add(expense)


@app.get("/expenses", response_model=list[Expense])
def list_expenses(category: Optional[str] = None):
    return store.list_all(category)


@app.get("/expenses/total")
def get_total(category: Optional[str] = None):
    return {"category": category, "total": store.total(category)}


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: str):
    deleted = store.delete(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return None
