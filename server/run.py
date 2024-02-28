#!/usr/bin/env python

"""
20.02.2024
Alexander Tyamin.

Server launch script (entry point).
"""

import sys
from pathlib import Path

import uvicorn

from server.root.settings import CONFIG

if __name__ == '__main__':
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    uvicorn.run(
        "root.asgi:app",
        host=CONFIG["HOST"],
        port=int(CONFIG["PORT"]),
        reload=bool(CONFIG["RELOAD"]),
    )
