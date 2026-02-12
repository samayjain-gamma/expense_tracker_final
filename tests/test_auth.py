import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_login_success(async_client):
    payload = {"email": "alice@example.com", "password": "12345678"}
    response = await async_client.post("/auth/login", data=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_failure(async_client):
    payload = {"email": "alice@example.com", "password": "wrongpassword"}
    response = await async_client.post("/auth/login", data=payload)
    assert response.status_code == 401
