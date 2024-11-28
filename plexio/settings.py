from pydantic_settings import BaseSettings

from plexio.cache import CacheType


class Settings(BaseSettings):
    cors_origin_regex: str = (
        r'https?:\/\/localhost:\d+|.*plexio.stream|.*strem.io|.*stremio.com'
    )
    plex_requests_timeout: int = 20
    cache_type: CacheType = CacheType.memory
    redis_url: str = 'redis://redis:6399/0'
    plex_matching_token: str | None = None


settings = Settings()
