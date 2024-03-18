"""
18.03.2024
Alexander Tyamin.

Tests for auth module.
"""

from fastapi.testclient import TestClient

from server.root.asgi import app

client = TestClient(app)


def test_normal_sign_up():
    response = client.post(
        "/v1/auth/sign-up",
        json={
            "name": "test",
            "email": "test@example.com",
            "password": "Master#chew123_$",
        },
    )

    client.delete("/v1/users")

    assert response.status_code == 200
