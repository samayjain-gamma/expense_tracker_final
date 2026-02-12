import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_get_expenses(async_client):
    response = await async_client.get("/expenses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


@pytest.mark.asyncio
async def test_create_expense(async_client):
    payload = {
        "user_id": 1,
        "expense_date": "2026-02-15",
        "amount": 100,
        "category": "FOOD",
        "description": "Dinner",
    }
    response = await async_client.post("/expenses/", json=payload)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_delete_expense(async_client):
    response = await async_client.get("/expenses/")
    expense_id = response.json()[0]["expense_id"]

    response = await async_client.delete(f"/expenses/{expense_id}")
    assert response.status_code == 204
