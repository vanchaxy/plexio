from uuid import uuid4

from pydantic_settings import BaseSettings

from plexio.cache import CacheType


class Settings(BaseSettings):
    identifier: str = str(uuid4())
    product_name: str = 'Plexio'
    cors_origin_regex: str = (
        r'https?:\/\/localhost:\d+|.*plexio.stream|.*strem.io|.*stremio.com'
    )
    plex_requests_timeout: int = 30
    cache_type: CacheType = CacheType.memory
    redis_url: str = 'redis://redis/0'
    plex_matching_token: str


settings = Settings()
