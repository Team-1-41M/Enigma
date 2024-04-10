import os

import pytest
from fastapi.testclient import TestClient
from server.root.asgi import app


@pytest.mark.asyncio
async def test_sign_in_normal():
    """
    Test: sign in normal mode.
    Also check if session cookie is set.
    Trying to login as superuser because it's the only user in the database.
    """

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/sign-in",
            json={
                "name": os.getenv("SUPERUSER_NAME"),
                "password": os.getenv("SUPERUSER_PASSWORD"),
            },
        )

        assert response.status_code == 200
        assert response.cookies.get("session")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, password",
    [
        (os.getenv("SUPERUSER_NAME"), "wrong_password"),
        ("wrong_name", os.getenv("SUPERUSER_PASSWORD")),
    ],
)
async def test_sign_in_wrong_credentials(name: str, password: str):
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/sign-in",
            json={
                "name": name,
                "password": password,
            },
        )

        assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, email",
    [
        (os.getenv("SUPERUSER_NAME"), "wrong_email@example.com"),
        ("wrong_name", os.getenv("SUPERUSER_EMAIL")),
    ],
)
async def test_sign_up_same_credentials(name: str, email: str):
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/sign-up",
            json={
                "name": name,
                "email": email,
                "password": os.getenv("SUPERUSER_PASSWORD"),
            },
        )

        assert response.status_code == 409
