from sqlalchemy import Column, Integer, Float, DateTime, Date, Enum, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base_class import Base
import enum


class ExpenseCategory(str, enum.Enum):
    FOOD = "food"
    TRAVEL = "travel"
    SHOPPING = "shopping"
    BILLS = "bills"
    ENTERTAINMENT = "entertainment"
    HEALTH = "health"
    EDUCATION = "education"
    RENT = "rent"
    SUBSCRIPTION = "subscription"
    OTHER = "other"


class Expense(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    expense_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(Enum(ExpenseCategory), nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
