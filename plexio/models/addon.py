from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)
from yarl import URL

from plexio.models.utils import to_camel

DEFAULT_QUALITIES = [
    {
        'name': '4k',
        'min_width': 3840,
        'plex_args': {
            'videoQuality': 100,
            'maxVideoBitrate': 64,
            'videoResolution': '3840x2160',
        },
    },
    {
        'name': '1080p',
        'min_width': 1920,
        'plex_args': {
            'videoQuality': 100,
            'maxVideoBitrate': 10,
            'videoResolution': '1920x1080',
        },
    },
    {
        'name': '720p',
        'min_width': 1280,
        'plex_args': {
            'videoQuality': 100,
            'maxVideoBitrate': 6.5,
            'videoResolution': '1280x720',
        },
    },
]


class AddonConfiguration(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        arbitrary_types_allowed=True,
    )

    access_token: str
    discovery_url: URL
    streaming_url: URL
    server_name: str
    installation_id: str
    version: str = '0.0.1'
    qualities: list = DEFAULT_QUALITIES

    _extract_discovery_url = field_validator('discovery_url', mode='before')(URL)
    _extract_streaming_url = field_validator('streaming_url', mode='before')(URL)
