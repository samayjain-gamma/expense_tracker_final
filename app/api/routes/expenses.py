import uuid
from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import and_, delete, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.category import ExpenseCategory
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseDelete, ExpenseResponse

# from uuid import UUID
router = APIRouter()


@router.post(
    "/",
    operation_id="expense_create",
    description="Creating an Expense",
    response_model=ExpenseResponse,
)
async def create_expense(
    expense_data: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_expense = Expense(
        user_id=current_user.user_id,
        expense_date=expense_data.expense_date,
        amount=expense_data.amount,
        category=expense_data.category.name,
        description=expense_data.description,
        created_at=datetime.utcnow(),
    )

    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)

    return new_expense


@router.get(
    "/",
    operation_id="view_expenses",
    description="Viewing Expenses",
    response_model=List[ExpenseResponse],
)
async def get_expenses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    amount: Optional[float] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    category: Optional[ExpenseCategory] = Query(None),
    expense_date: Optional[date] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    conditions = [Expense.user_id == current_user.user_id]

    if amount is not None:
        conditions.append(Expense.amount == amount)
    if min_amount is not None:
        conditions.append(Expense.amount >= min_amount)
    if max_amount is not None:
        conditions.append(Expense.amount <= max_amount)
    if category is not None:
        conditions.append(Expense.category == category.name)
    if expense_date is not None:
        conditions.append(Expense.expense_date == expense_date)
    if start_date is not None:
        conditions.append(Expense.expense_date >= start_date)
    if end_date is not None:
        conditions.append(Expense.expense_date <= end_date)

    query = (
        select(Expense).where(and_(*conditions)).order_by(Expense.expense_date.desc())
    )

    result = await db.execute(query)
    expenses = result.scalars().all()

    return expenses


@router.delete(
    "/",
    operation_id="delete_expenses",
    description="Delete single or multiple expenses",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_expenses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    expense_id: Optional[uuid.UUID] = Query(
        None, description="Delete by specific expense ID"
    ),
    amount: Optional[float] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    category: Optional[ExpenseCategory] = Query(None),
    expense_date: Optional[date] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    if expense_id:
        query = select(Expense).where(
            Expense.expense_id == expense_id,
            Expense.user_id == current_user.user_id,
        )
        result = await db.execute(query)
        expense = result.scalar_one_or_none()
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        await db.delete(expense)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    conditions = [Expense.user_id == current_user.user_id]
    if amount is not None:
        conditions.append(Expense.amount == amount)
    if min_amount is not None:
        conditions.append(Expense.amount >= min_amount)
    if max_amount is not None:
        conditions.append(Expense.amount <= max_amount)
    if category is not None:
        conditions.append(Expense.category == category)
    if expense_date is not None:
        conditions.append(Expense.expense_date == expense_date)
    if start_date is not None:
        conditions.append(Expense.expense_date >= start_date)
    if end_date is not None:
        conditions.append(Expense.expense_date <= end_date)

    stmt = delete(Expense).where(and_(*conditions))
    result = await db.execute(stmt)
    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="No expenses found to delete")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
