"""
23.02.2024
Alexander Tyamin.

Storage for processing cache, user sessions, and any key-value data.
"""

from abc import ABC, abstractmethod


class CacheStorage(ABC):
    """Provides a key-value storage."""

    @abstractmethod
    async def get(self, key):
        pass

    @abstractmethod
    async def set(self, key, value):
        pass

    @abstractmethod
    async def delete(self, key):
        pass


async def get_cache_storage() -> CacheStorage:
    """
    Provides a key-value storage.

    return: CacheStorage interface
    """

    storage = {}
    yield storage
