"""
23.02.2024
Alexander Tyamin.

Constants for the project: prefixes, urls, etc.
"""

from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent

SESSION_TTL = 3 * 24 * 60 * 60

DB_PATH = BASE_PATH / "enigma.sqlite3"
DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"
