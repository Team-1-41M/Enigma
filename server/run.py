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

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    uvicorn.run(
        "root.asgi:app",
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        reload=bool(os.getenv("RELOAD")),
    )
