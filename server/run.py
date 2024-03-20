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

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    from root.settings import ENVS_PATH

    load_dotenv(ENVS_PATH / ".debug")

    if os.getenv("DEBUG") == "True":
        ENV_PATH = "local"
    else:
        load_dotenv()
        ENV_PATH = "docker"

    RUNNING_ENV_PATH = ENVS_PATH / ENV_PATH

    load_dotenv(RUNNING_ENV_PATH / ".db")
    load_dotenv(RUNNING_ENV_PATH / ".server")

    uvicorn.run(
        "root.asgi:app",
        host=os.getenv("SERVER_HOST"),
        port=int(os.getenv("SERVER_PORT")),
        reload=bool(os.getenv("SERVER_RELOAD")),
    )
