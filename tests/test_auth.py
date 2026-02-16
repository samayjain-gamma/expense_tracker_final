import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_register_user(client: AsyncClient, async_session):

    payload = {
        "email": "charlie@test.com",
        "username": "charlie",
        "password": "password3",
    }
    response = await client.post("/api/auth/register", json=payload)
    assert response.status_code == 201


@pytest.mark.anyio
async def test_login_success(client: AsyncClient, preloaded_users):
    payload = {"email": "alice@test.com", "password": "password1"}
    response = await client.post("/api/auth/login", data=payload)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_login_failure(client: AsyncClient):
    payload = {"email": "alice@test.com", "password": "wrongpassword"}
    response = await client.post("/api/auth/login", data=payload)
    assert response.status_code == 422

    payload = {"email": "nonexistent@test.com", "password": "any"}
    response = await client.post("/api/auth/login", data=payload)
    assert response.status_code == 422
