from abc import ABC, abstractmethod
from enum import Enum

from redis.asyncio import Redis


def init_cache(settings):
    if settings.cache_type is CacheType.memory:
        return MemoryCache()
    if settings.cache_type is CacheType.redis:
        return RedisCache(settings.redis_url)
    raise NotImplementedError(f'Cache type {settings.cache_type} not implemented')


class CacheType(Enum):
    memory = 'memory'
    redis = 'redis'


class AbstractCache(ABC):
    @abstractmethod
    async def set(self, key, value):
        pass

    @abstractmethod
    async def get(self, key):
        pass

    @abstractmethod
    async def close(self):
        pass


class MemoryCache(AbstractCache):
    def __init__(self):
        self._cache = {}

    async def set(self, key, value):
        self._cache[key] = value

    async def get(self, key):
        return self._cache.get(key)

    async def close(self):
        pass


class RedisCache(AbstractCache):
    def __init__(self, redis_url):
        self._redis = Redis.from_url(url=redis_url)

    async def set(self, key, value):
        await self._redis.set(key, value)

    async def get(self, key):
        if value := await self._redis.get(key):
            return value.decode()
        return None

    async def close(self):
        await self._redis.close()
