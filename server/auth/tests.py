import os

from fastapi.testclient import TestClient
from starlette import status

from run import app

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
            "name": os.getenv("SUPERUSER_NAME"),
            "password": os.getenv("SUPERUSER_PASSWORD"),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.cookies["session"]
