from fastapi import APIRouter

from app.api.routes import auth, expenses

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])

router.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])

# router.include_router(
#     budget.router,
#     prefix="/budget",
#     tags=["Budget"]
# )
