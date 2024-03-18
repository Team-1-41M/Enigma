"""
18.03.2024
Alexander Tyamin.

Tests for auth module.
"""

from fastapi.testclient import TestClient

from server.root.asgi import app

client = TestClient(app)


def test_normal_sign_in():
    response = client.post(
        "api/v1/auth/sign-in",
        json={
            "name": "test",
            "password": "Master#chew123_$",
        },
    )

    assert response.status_code == 200
