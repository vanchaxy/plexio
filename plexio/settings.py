from pydantic_settings import BaseSettings

from plexio.cache import CacheType


class Settings(BaseSettings):
    identifier: str = '9500ce72-c314-4453-959c-dfab96e222a4'
    product_name: str = 'Plexio'
    cors_origin_regex: str = (
        r'https?:\/\/localhost:\d+|.*plexio.stream|.*strem.io|.*stremio.com'
    )
    plex_requests_timeout: int = 5
    cache_type: CacheType = CacheType.memory
    redis_url: str = 'redis://redis/0'


settings = Settings()
