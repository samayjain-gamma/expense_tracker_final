from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete

from datetime import datetime, timezone, date
from typing import Optional, List

from app.api.deps import get_db, get_current_user
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.models.category import ExpenseCategory


router = APIRouter()

@router.post(
    "/",
    operation_id="expense_create",
    description= "Creating an Expense",
    response_model=ExpenseResponse,
)
async def  create_expense(
        expense_data : ExpenseCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)       
):
    new_expense = Expense(
        user_id=current_user.user_id,
        expense_date=expense_data.expense_date,
        amount=expense_data.amount,
        category=expense_data.category.name,
        description=expense_data.description,
        created_at=datetime.utcnow()
    )

    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)

    return new_expense



@router.get(
    "/",
    operation_id="view_expenses",
    description="Viewing Expenses",
    response_model=List[ExpenseResponse]
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

    query = select(Expense).where(and_(*conditions)).order_by(Expense.expense_date.desc())

    result = await db.execute(query)
    expenses = result.scalars().all()

    return expenses



@router.delete(
    "/",
    operation_id="delete_expense",
    description="Deleting an Expense"
)
async def delete_expenses(
    expense_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Expense).where(
        Expense.expense_id == expense_id,
        Expense.user_id == current_user.user_id
    )

    result = await db.execute(query)
    expense = result.scalar_one_or_none()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    await db.delete(expense)
    await db.commit()

    return None
