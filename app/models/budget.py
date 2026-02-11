from sqlalchemy import Column, Integer, Float, String ,Enum, ForeignKey, DateTime
from app.db.base_class import Base
import enum
from datetime import datetime, timezone
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


class Budget(Base):
    __tablename__ = "budgets"

    budget_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    limit = Column(Float, nullable=False)
    category = Column(Enum(ExpenseCategory), nullable=False)
    remaining_limit = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
