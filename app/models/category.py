import enum

from sqlalchemy import Enum


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
