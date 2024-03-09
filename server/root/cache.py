"""
23.02.2024
Alexander Tyamin.

Storage for processing cache, user sessions, and any key-value data.
"""

from typing import Hashable, Any
from abc import ABC, abstractmethod


class CacheStorage(ABC):
    """Provides a key-value storage."""

    @abstractmethod
    async def get(self, key: Hashable) -> Any:
        """
        Provides a value by a key.

        Args:
            key: key as a hashable object.

        Returns:
            Any: value.
        """

        pass

    @abstractmethod
    async def set(self, key: Hashable, value: Any) -> None:
        """
        Sets a value by a key.

        Args:
            key: key as a hashable object.
            value: value to set with the key.

        Returns:
            None.
        """

        pass

    @abstractmethod
    async def delete(self, key: Hashable) -> None:
        """
        Deletes a value by a key.

        Args:
            key: key as a hashable object.

        Returns:
            None.
        """

        pass

    @abstractmethod
    async def expire(self, key: Hashable, ttl: int) -> None:
        """
        Allows to set the lifetime of the key.

        Args:
            key: key as a hashable object.
            ttl: time to live in seconds.

        Returns:
            None.
        """

        pass


class DictCacheStorage(CacheStorage):
    """
    Provides a key-value storage
    based on a standard Python dictionary.
    """

    def __init__(self) -> None:
        """Initializes a new instance of the DictCacheStorage class."""

        super().__init__()

        self.storage = {}

    async def get(self, key: Hashable) -> Any:
        return self.storage.get(key)

    async def set(self, key: Hashable, value: Any) -> None:
        self.storage[key] = value

    async def delete(self, key: Hashable) -> None:
        self.storage.pop(key, None)

    async def expire(self, key: Hashable, ttl: int) -> None:
        pass


storage = DictCacheStorage()


async def get_cache_storage() -> CacheStorage:
    """
    Provides a key-value storage.

    Returns:
        CacheStorage: key-value storage
    """

    return storage
