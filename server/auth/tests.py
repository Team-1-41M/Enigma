import os

import pytest
from fastapi.testclient import TestClient
from server.root.asgi import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_sign_in_normal():
    """
    Test: sign in normal mode. 
    Also check if session cookie is set.
    Trying to login as superuser because it's the only user in the database.
    """

    response = client.post(
        "/api/v1/auth/sign-in",
        json={
            "name": os.getenv("SUPERUSER_NAME"),
            "password": os.getenv("SUPERUSER_PASSWORD"),
        }
    )

    assert response.status_code == 200
    assert response.cookies.get("session")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, password",
    [
        (os.getenv("SUPERUSER_NAME"), "wrong_password"),
        ("wrong_name", os.getenv("SUPERUSER_PASSWORD")),
    ]
)
async def test_sign_in_wrong_credentials(name: str, password: str):
    response = client.post(
        "/api/v1/auth/sign-in",
        json={
            "name": name,
            "password": password,
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_sign_up_same_name():
    pass
