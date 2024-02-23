#!/usr/bin/env python

"""
20.02.2024
Alexander Tyamin.

Server launch script (entry point).
"""

import sys

import uvicorn

from core.settings import BASE_PATH

if __name__ == '__main__':
    sys.path.append(BASE_PATH)

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
