import os
from abc import ABC, abstractmethod
from typing import Any, Hashable

if os.getenv("CACHE_TYPE") == "redis":
    from redis.asyncio import Redis


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


class RedisCacheStorage(CacheStorage):
    # TODO: how to close connection like self.storage.aclose()?

    """
    Provides a key-value storage
    based on Redis.
    """

    def __init__(self, host: str, port: int, db: int) -> None:
        """Initializes a new instance of the RedisCacheStorage class."""

        super().__init__()

        self.storage = Redis(host=host, port=port, db=db)

    async def get(self, key: Hashable) -> Any:
        return await self.storage.get(key)

    async def set(self, key: Hashable, value: Any) -> None:
        await self.storage.set(key, value)

    async def delete(self, key: Hashable) -> None:
        await self.storage.delete(key)


match os.getenv("CACHE_TYPE"):
    case "dict":
        storage = DictCacheStorage()
    case "redis":
        storage = RedisCacheStorage(
            os.getenv("CACHE_HOST"),
            int(os.getenv("CACHE_PORT")),
            int(os.getenv("CACHE_DB")),
        )
    case _:
        storage = DictCacheStorage()


clients = DictCacheStorage()


async def get_clients_storage() -> CacheStorage:
    return clients


async def get_cache_storage() -> CacheStorage:
    """
    Provides a key-value storage.

    Returns:
        CacheStorage: key-value storage.
    """

    return storage
