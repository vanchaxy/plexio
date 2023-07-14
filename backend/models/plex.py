from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from backend.models.utils import to_camel


class AuthPin(BaseModel):
    id: int
    code: str


class PlexUser(BaseModel):
    username: str
    thumb: str


class PlexServer(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    name: str
    source_title: str | None
    public_address: str
    access_token: str
    relay: bool
    https_required: bool
    connections: list


class PlexMediaType(str, Enum):
    show = 'show'
    movie = 'movie'
    episode = 'episode'


class PlexLibrarySection(BaseModel):
    key: str
    title: str
    type: PlexMediaType


class PlexMediaMeta(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    key: str
    guid: str
    type: PlexMediaType
    title: str
    year: int | None = None
    summary: str
    thumb: str
    art: str | None = None
    section: str | None = Field(alias='librarySectionTitle', default=None)
    guids: list = Field(alias='Guid', default_factory=list)
    audience_rating: float | None = None
    originally_available_at: str | None = None
    added_at: int
    updated_at: int | None = None
    duration: int | None = None
    genres: list = Field(alias='Genre', default_factory=list)
    countries: list = Field(alias='Country', default_factory=list)
    directors: list = Field(alias='Director', default_factory=list)
    writers: list = Field(alias='Writer', default_factory=list)
    cast: list = Field(alias='Role', default_factory=list)


class PlexEpisodeMeta(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    guid: str
    title: str
    originally_available_at: str
    thumb: str
    episode: int = Field(alias='index')
    season: int = Field(alias='parentIndex')
    summary: str
