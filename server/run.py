#!/usr/bin/env python

"""
20.02.2024
Alexander Tyamin.

Server launch script (entry point).
"""

import os
import sys
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

load_dotenv()

sys.path.append(str(Path(__file__).resolve().parent.parent))

from server.root.asgi import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv("SERVER_HOST"),
        port=int(os.getenv("SERVER_PORT")),
        reload=bool(os.getenv("SERVER_RELOAD")),
    )
