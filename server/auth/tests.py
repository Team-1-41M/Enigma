"""
18.03.2024
Alexander Tyamin.

Tests for auth module.
"""

from starlette import status
from fastapi.testclient import TestClient

from server.root.asgi import app

client = TestClient(app)


def test_sign_in_normal() -> None:
    """
    Test normal sign in process with correct credentials.

    Args:
        None.

    Returns:
        None.
    """

    response = client.post(
        "api/v1/auth/sign-in",
        json={
            "name": "test",
            "password": "Master#chew123_$",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.cookies["session"]


def test_sign_in_wrong_name() -> None:
    """
    Test sign in process with wrong user name.

    Args:
        None.

    Returns:
        None.
    """

    response = client.post(
        "api/v1/auth/sign-in",
        json={
            "name": "notexist",
            "password": "Master#chew123_$",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_sign_in_wrong_password() -> None:
    """
    Test sign in process with wrong user password.

    Args:
        None.

    Returns:
        None.
    """

    response = client.post(
        "api/v1/auth/sign-in",
        json={
            "name": "test",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_sign_up_same_name() -> None:
    """
    Test attempt to register a user with the name of an already registered user.

    Args:
        None.

    Returns:
        None.
    """

    response = client.post(
        "api/v1/auth/sign-up",
        json={
            "name": "test",
            "email": "a@a.ru",
            "password": "Master#chew123_$",
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_sign_up_same_email() -> None:
    """
    Test attempt to register a user with the email of an already registered user.

    Args:
        None.

    Returns:
        None.
    """

    response = client.post(
        "api/v1/auth/sign-up",
        json={
            "name": "test1",
            "email": "test@example.com",
            "password": "Master#chew123_$",
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
