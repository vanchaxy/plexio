import asyncio
from abc import ABC, abstractmethod
from enum import Enum

from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError

PLEX_CACHE_TTL = 24 * 60 * 60


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
    RETRY_TIMES = 3
    RETRY_BACKOFF_SEC = 1

    def __init__(self, redis_url):
        self._redis = Redis.from_url(url=redis_url)

    async def set(self, key, value):
        for _ in range(RedisCache.RETRY_TIMES):
            try:
                await self._redis.set(key, value, ex=PLEX_CACHE_TTL)
            except RedisConnectionError:
                await asyncio.sleep(RedisCache.RETRY_BACKOFF_SEC)

    async def get(self, key):
        for _ in range(RedisCache.RETRY_TIMES):
            try:
                if value := await self._redis.get(key):
                    return value.decode()
                return None
            except RedisConnectionError:
                await asyncio.sleep(RedisCache.RETRY_BACKOFF_SEC)

    async def close(self):
        await self._redis.close()
