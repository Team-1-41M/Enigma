#!/usr/bin/env python

"""
20.02.2024
Alexander Tyamin.

Server launch script (entry point).
"""

import uvicorn

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
