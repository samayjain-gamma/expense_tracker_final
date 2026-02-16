import pytest

from app.db.session import SessionLocal


@pytest.mark.asyncio
async def test_session_creation():
    async with SessionLocal() as session:
        assert session is not None
