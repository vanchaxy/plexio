from pydantic import field_validator
from pydantic_settings import BaseSettings
from yarl import URL


class Settings(BaseSettings):
    identifier: str = '9500ce72-c314-4453-959c-dfab96e222a4'
    product_name: str = '[BETA] Plexio'
    cors_origin_regex: str = r'https?:\/\/localhost:\d+|.*plexio.stream|.*strem.io'
    matching_plex_address: URL = 'http://127.0.0.1:32400'
    redis_host: str = 'redis'

    _extract_matching_plex_address = field_validator(
        'matching_plex_address',
        mode='before',
    )(URL)


settings = Settings()
