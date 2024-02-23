"""
23.02.2024
Alexander Tyamin.

Crypt context for hashing passwords.
"""

from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
