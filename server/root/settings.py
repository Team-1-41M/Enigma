"""
23.02.2024
Alexander Tyamin.

Constants for the project, shared for different apps.
"""

from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent

SESSION_TTL = 3 * 24 * 60 * 60
