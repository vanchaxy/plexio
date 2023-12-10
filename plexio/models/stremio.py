from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from plexio.models.utils import to_camel


class StremioMediaType(str, Enum):
    series = 'series'
    movie = 'movie'


class StremioCatalogManifest(BaseModel):
    id: str
    name: str
    type: StremioMediaType
    extra: list[dict]


class StremioManifest(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    id: str
    version: str
    description: str
    name: str
    resources: list[str | dict]
    types: list[StremioMediaType]
    catalogs: list[StremioCatalogManifest]
    id_prefixes: list[str]
    behavior_hints: dict
    contact_email: str


class StremioVideoMeta(BaseModel):
    id: str
    title: str
    released: str
    thumbnail: str
    episode: int
    season: int
    overview: str


class StremioMeta(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    id: str
    type: StremioMediaType
    name: str
    description: str
    poster: str
    background: str | None = None
    videos: list[StremioVideoMeta] | None = None
    release_info: str
    imdb_rating: float | None = None


class StremioMetaResponse(BaseModel):
    meta: StremioMeta


class StremioMetaPreview(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    id: str
    name: str
    release_info: str | None = None
    poster: str
    type: StremioMediaType
    imdb_rating: float | None = None
    description: str
    genres: list[str]


class StremioCatalog(BaseModel):
    metas: list[StremioMetaPreview]


class StremioStream(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    name: str
    title: str
    url: str
    behavior_hints: dict = Field(default_factory=dict)


class StremioStreamsResponse(BaseModel):
    streams: list[StremioStream] = Field(default_factory=list)
