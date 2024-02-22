"""
20.02.2024
Alexander Tyamin.

This file contains the FastAPI application instance.
"""

from fastapi import FastAPI, WebSocket

app = FastAPI()

project = '''{ "elements":[ { "id":1, "attributes":{ "name":"Element 1", "x":0, "y":0, "width":100, "height":100 } }, { "id":1, "attributes":{ "name":"Element 1", "x":0, "y":0, "width":100, "height":100 } } ] }'''

clients = set()


@app.websocket("/project")
async def process(socket: WebSocket) -> None:
    """
    Collects project status changes from the client
    and notifies other clients about this.

    :param socket: a WebSocket object from FastAPI.
    :return: None.
    """
    global project

    await socket.accept()
    clients.add(socket)

    await socket.send_text(project)

    while True:
        project = await socket.receive_text()

        for client in clients:
            if client != socket:
                await client.send_text(project)
