"""
23.02.2024
Alexander Tyamin.

Helper functions for working for users identification.
"""

from passlib.context import CryptContext


async def verify_password(
        plain_password: str,
        hashed_password: str,
        crypt_context: CryptContext,
) -> bool:
    """
    Verify hashed password.

    params:
        plain_password: raw user password
        hashed_password: hashed password stored in the database
        crypt_context: helper with hashing algorithms

    :return bool: True if passwords match, False otherwise.
    """

    return crypt_context.verify(plain_password, hashed_password)
