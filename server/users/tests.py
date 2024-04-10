from fastapi.testclient import TestClient
from server.root.asgi import app


def test_me_session_not_provided():
    with TestClient(app) as client:
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401
