# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select, and_, delete, func

# from datetime import datetime, date
# from typing import Optional, List

# from app.api.deps import get_db, get_current_user
# from app.models.budget import Budget as BudgetModel
# from app.schemas.budget import (BudgetCreate, BudgetResponse)
# from app.models.user import User
# from app.models.expense import Expense as ExpenseModel

# router = APIRouter()

# @router.post(
#     "/",
#     operation_id="budget_create",
#     description="Creating a Budget",
#     response_model=BudgetResponse
# )
# async def create_budget(
#     budget_data : BudgetCreate,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     result = await db.execute(
#         select(BudgetModel).where(
#             BudgetModel.user_id == current_user.user_id,
#             BudgetModel.category == budget_data.category
#         )
#     )
#     existing_budget = result.scalar_one_or_none()

#     if existing_budget:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Budget for category {budget_data.category} already exist with limit {existing_budget.limit} and remaining {existing_budget.remaining_limit}"
#         )
#     result = await db.execute(
#         select(func.coalesce(func.sum(ExpenseModel.amount), 0)).where(
#             ExpenseModel.user_id == current_user.user_id,
#             ExpenseModel.category == budget_data.category
#         )
#     )
#     total_expenses = result.scalar()

#     remaining_budget = budget_data.limit - total_expenses

#     if remaining_budget < 0:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Cannot create budget. Expenses for this category already exceed the proposed limit."
#         )

#     budget = BudgetModel(
#         user_id = current_user.user_id,
#         limit = budget_data.limit,
#         category = budget_data.category,
#         remaining_limit = remaining_budget
#     )

#     db.add(budget)
#     await db.commit()
#     await db.refresh(budget)

#     return budget
