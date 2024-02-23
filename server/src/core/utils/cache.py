"""
23.02.2024
Alexander Tyamin.

Storage for processing cache, user sessions, and any key-value data.
"""


async def get_cache_storage():
    """Provides a key-value storage."""

    storage = {}
    yield storage
