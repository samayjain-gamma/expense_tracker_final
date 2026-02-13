import asyncio
import uuid
from datetime import date, datetime, timezone

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.core.security import hash_password
from app.db.base_class import Base
from app.main import app
from app.models.category import ExpenseCategory
from app.models.expense import Expense
from app.models.user import User


@pytest_asyncio.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture()
async def async_session(test_engine):
    async_session_maker = async_sessionmaker(bind=test_engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def override_get_db(async_session):
    async def _override_get_db():
        yield async_session

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def client(override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest_asyncio.fixture()
async def preloaded_users(async_session):
    users = [
        User(
            email="alice@test.com",
            username="alice",
            password_hash=hash_password("password1"),
        ),
        User(
            email="bob@test.com",
            username="bob",
            password_hash=hash_password("password2"),
        ),
    ]
    async_session.add_all(users)
    await async_session.commit()
    for user in users:
        await async_session.refresh(user)
    return users


@pytest_asyncio.fixture()
async def preloaded_expenses(async_session, preloaded_users):
    expenses = [
        Expense(
            expense_id=str(uuid.uuid4()),
            user_id=preloaded_users[0].user_id,
            amount=100.0,
            expense_date=date.today(),
            category=ExpenseCategory.FOOD,
            description="Lunch",
        ),
        Expense(
            expense_id=str(uuid.uuid4()),
            user_id=preloaded_users[0].user_id,
            amount=200.0,
            expense_date=date.today(),
            category=ExpenseCategory.TRAVEL,
            description="Taxi",
        ),
        Expense(
            expense_id=str(uuid.uuid4()),
            user_id=preloaded_users[1].user_id,
            amount=50.0,
            expense_date=date.today(),
            category=ExpenseCategory.ENTERTAINMENT,
            description="Movie",
        ),
    ]
    async_session.add_all(expenses)
    await async_session.commit()
    for exp in expenses:
        await async_session.refresh(exp)
    return expenses
