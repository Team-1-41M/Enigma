"""
23.02.2024
Alexander Tyamin.

Constants for the project: prefixes, urls, etc.
"""

from pathlib import Path

from dotenv import dotenv_values

BASE_PATH = Path(__file__).resolve().parent.parent.parent

CONFIG = dotenv_values(BASE_PATH / ".env")

SESSION_TTL = 3 * 24 * 60 * 60
