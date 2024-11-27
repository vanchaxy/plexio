from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from plexio.models.utils import to_camel


class StremioBase(BaseModel):
    pass


class StremioMediaType(str, Enum):
    series = 'series'
    movie = 'movie'


class StremioPosterShape(str, Enum):
    square = 'square'  # 1:1
    poster = 'poster'  # 1:0.675
    landscape = 'landscape'  # 1:1.77


class StremioMetaLinkCategory(str, Enum):
    actor = 'actor'
    director = 'director'
    writer = 'writer'


class StremioCatalogManifest(StremioBase):
    id: str
    name: str
    type: StremioMediaType
    extra: list[dict]


class StremioManifest(StremioBase):
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


class StremioStreamBehaviorHints(StremioBase):
    model_config = ConfigDict(alias_generator=to_camel)

    country_whitelist: list | None = None
    not_web_ready: bool = False
    binge_group: str | None = None
    proxy_headers: dict | None = None


class StremioStream(StremioBase):
    model_config = ConfigDict(alias_generator=to_camel)

    url: str | None = None
    ytId: str | None = None
    infoHash: str | None = None
    fileIdx: str | None = None
    external_url: str | None = None

    name: str
    description: str
    subtitles: list | None = None
    behavior_hints: StremioStreamBehaviorHints | None = None


class StremioMetaLink(StremioBase):
    name: str
    category: StremioMetaLinkCategory
    url: str


class StremioVideoMeta(StremioBase):
    id: str
    title: str
    released: str
    streams: list[StremioStream] = Field(default_factory=list)
    available: bool = True
    thumbnail: str | None = None
    episode: int | None = None
    season: int | None = None
    trailers: list[StremioStream] = Field(default_factory=list)
    overview: str | None = None


class StremioMetaPreview(StremioBase):
    model_config = ConfigDict(alias_generator=to_camel)

    id: str
    type: StremioMediaType
    name: str
    poster: str | None = None
    poster_shape: StremioPosterShape = StremioPosterShape.poster
    genres: list[str] = Field(default_factory=list)
    imdb_rating: float | None = None
    release_info: str | None = None
    links: list[StremioMetaLink] = Field(default_factory=list)
    description: str | None = None


class StremioMeta(StremioBase):
    model_config = ConfigDict(alias_generator=to_camel)

    id: str
    type: StremioMediaType
    name: str
    genres: list[str] = Field(default_factory=list)
    poster: str | None = None
    poster_shape: StremioPosterShape = StremioPosterShape.poster
    background: str | None = None
    logo: str | None = None
    description: str | None = None
    release_info: str | None = None
    imdb_rating: float | None = None
    released: str | None = None
    links: list[StremioMetaLink] = Field(default_factory=list)
    videos: list[StremioVideoMeta] | None = None
    runtime: str | None = None
    language: str | None = None
    country: str | None = None
    awards: str | None = None
    website: str | None = None
    behavior_hints: dict = Field(default_factory=dict)


class StremioMetaResponse(StremioBase):
    meta: StremioMeta


class StremioCatalog(StremioBase):
    metas: list[StremioMetaPreview]


class StremioStreamsResponse(StremioBase):
    streams: list[StremioStream] = Field(default_factory=list)
