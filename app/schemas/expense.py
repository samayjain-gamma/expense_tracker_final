from pydantic import BaseModel, Field
from datetime import date, datetime
import enum
from app.models.category import ExpenseCategory

class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    expense_date: date
    category: ExpenseCategory
    description: str | None 



class ExpenseResponse(BaseModel):
    expense_id: int
    expense_date: date
    amount : float
    user_id: int
    created_at: datetime
    description: str | None

class ExpenseDelete(BaseModel):
    expense_id: int
