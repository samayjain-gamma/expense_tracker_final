from pydantic import BaseModel, Field
from datetime import datetime
from app.models.category import ExpenseCategory


class Budget(BaseModel):
    limit: float
    category: str


class BudgetCreate(BaseModel):
    limit: float
    category: ExpenseCategory


class BudgetResponse(BaseModel):
    budget_id: int
    category: ExpenseCategory
    limit: float
    remaining_limit: float
    created_at: datetime

class BudgetDelete(BaseModel):
    budget_id: int