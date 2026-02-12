import asyncio
import uuid
from datetime import date, datetime, timezone

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.deps import get_db
from app.core.security import hash_password
from app.db.base_class import Base
from app.main import app
from app.models.expense import Expense, ExpenseCategory
from app.models.user import User

pytestmark = pytest.mark.asyncio

DATABASE_URL = "sqlite+aiosqlite:///./tests/test.db"
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_users(session: AsyncSession):
    user1 = User(
        username="Alice",
        email="alice@example.com",
        password_hash=hash_password("12345678"),
    )
    user2 = User(
        username="Bob", email="bob@example.com", password_hash=hash_password("12345678")
    )
    session.add_all([user1, user2])
    await session.commit()
    await session.refresh(user1)
    await session.refresh(user2)
    return user1, user2


async def create_expenses(session: AsyncSession, users):
    user1, user2 = users
    expense1 = Expense(
        expense_id=uuid.uuid4(),
        user_id=user1.user_id,
        expense_date=date(2026, 2, 12),
        amount=50.0,
        category=ExpenseCategory.FOOD,
        description="Lunch at cafe",
        created_at=datetime.now(timezone.utc),
    )
    expense2 = Expense(
        expense_id=uuid.uuid4(),
        user_id=user2.user_id,
        expense_date=date(2026, 2, 11),
        amount=200.0,
        category=ExpenseCategory.HEALTH,
        description="Gym membership",
        created_at=datetime.now(timezone.utc),
    )
    session.add_all([expense1, expense2])
    await session.commit()
    await session.refresh(expense1)
    await session.refresh(expense2)
    return expense1, expense2


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    await create_tables()
    async with AsyncSessionLocal() as session:
        users = await create_users(session)
        await create_expenses(session, users)
    yield
    await drop_tables()


@pytest.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def async_client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
