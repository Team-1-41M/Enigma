"""
23.02.2024
Alexander Tyamin.

Constants for the project: prefixes, urls, etc.
"""

from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent

API_PREFIX = '/api'
API_VERSION_1_PREFIX = API_PREFIX + '/v1'

AUTH_ROUTER_PREFIX = '/auth'

ME_URL = '/me'
SIGN_UP_URL = '/sign-up'
SIGN_IN_URL = '/sign-in'
SIGN_OUT_URL = '/sign-out'

SESSION_TTL = 3 * 24 * 60 * 60

DB_PATH = BASE_PATH / "enigma.sqlite3"
DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"
