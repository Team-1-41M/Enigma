#!/usr/bin/env python

import os
import sys
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))
    RELOAD = os.getenv("RELOAD") == "True"
    WORKERS_AMOUNT = 1 if RELOAD else os.cpu_count() + 1

    uvicorn.run(
        "root.asgi:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        workers=WORKERS_AMOUNT,
    )
