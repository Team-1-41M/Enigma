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

    uvicorn.run(
        "root.asgi:app",
        host=os.getenv("SERVER_HOST"),
        port=int(os.getenv("SERVER_PORT")),
        reload=os.getenv("SERVER_RELOAD") == "True",
        workers=os.cpu_count() + 1 if os.getenv("SERVER_RELOAD") == "False" else 1,
    )
