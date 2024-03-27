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

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    HOST = os.getenv("SERVER_HOST")
    PORT = int(os.getenv("SERVER_PORT"))
    RELOAD = os.getenv("SERVER_RELOAD") == "True"
    WORKERS_AMOUNT = 1 if RELOAD else os.cpu_count() + 1

    uvicorn.run(
        "root.asgi:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        workers=WORKERS_AMOUNT,
    )
