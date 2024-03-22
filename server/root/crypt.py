from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_crypt_context():
    """Provides a crypt context for secure operations."""

    return crypt_context
