"""
20.02.2024
Alexander Tyamin.

This file contains the FastAPI application instance.
"""

from fastapi import FastAPI, WebSocket

app = FastAPI()

project = '''{ "elements":[ { "id":1, "attributes":{ "name":"Element 1", "x":0, "y":0, "width":100, "height":100 } }, { "id":1, "attributes":{ "name":"Element 1", "x":0, "y":0, "width":100, "height":100 } } ] }'''
