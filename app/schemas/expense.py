import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.category import ExpenseCategory


class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    expense_date: date
    category: ExpenseCategory
    description: str | None = None


class ExpenseResponse(BaseModel):
    expense_id: uuid.UUID
    expense_date: date
    amount: float
    user_id: int
    category: str
    description: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExpenseDelete(BaseModel):
    expense_id: uuid.UUID
