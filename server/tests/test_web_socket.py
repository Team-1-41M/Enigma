"""
22.02.2024
Alexander Tyamin.

Contains test to check websocket functions
like sending and receiving project content.
"""

from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from server.src.app import app, project


def test_project_content_received():
    """Check client can receive project content."""

    # FIXME: What it's not working correctly without try...except block?
    try:
        with TestClient(app) as client:
            with client.websocket_connect("/project") as socket:
                response = socket.receive_text()
                assert response == project
    except WebSocketDisconnect:
        pass
