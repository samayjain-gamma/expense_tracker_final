from datetime import datetime

from pydantic import BaseModel, Field

from app.models.category import ExpenseCategory

# class BudgetCategory(enum.Enum):
#     FOOD = "food"
#     TRAVEL = "travel"
#     SHOPPING = "shopping"
#     BILLS = "bills"
#     ENTERTAINMENT = "entertainment"
#     HEALTH = "health"
#     EDUCATION = "education"
#     RENT = "rent"
#     SUBSCRIPTION = "subscription"
#     OTHER = "other"


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
