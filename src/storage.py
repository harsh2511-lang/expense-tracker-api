from typing import Optional
from src.models import Expense, ExpenseCreate


class ExpenseStore:
    """Simple in-memory store. A dict keyed by id gives O(1) lookup/delete
    instead of scanning a list every time."""

    def __init__(self):
        self._expenses: dict[str, Expense] = {}

    def add(self, data: ExpenseCreate) -> Expense:
        expense = Expense(**data.model_dump())
        self._expenses[expense.id] = expense
        return expense

    def list_all(self, category: Optional[str] = None) -> list[Expense]:
        values = list(self._expenses.values())
        if category:
            values = [e for e in values if e.category.lower() == category.lower()]
        return values

    def delete(self, expense_id: str) -> bool:
        if expense_id in self._expenses:
            del self._expenses[expense_id]
            return True
        return False

    def total(self, category: Optional[str] = None) -> float:
        values = self.list_all(category)
        return round(sum(e.amount for e in values), 2)



store = ExpenseStore()
