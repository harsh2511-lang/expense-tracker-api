from pydantic import BaseModel, Field
from datetime import date as date_type
import uuid


class ExpenseCreate(BaseModel):
    """What the client sends us when adding a new expense.
    No 'id' here -- the server generates that."""
    title: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)  # must be positive
    category: str = Field(..., min_length=1)
    date: date_type


class Expense(ExpenseCreate):
    """What we store and return -- adds the server-generated id."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
