from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)
from yarl import URL

from backend.models.utils import to_camel


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

    _extract_discovery_url = field_validator('discovery_url', mode='before')(URL)
    _extract_streaming_url = field_validator('streaming_url', mode='before')(URL)
