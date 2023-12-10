from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from plexio.models.utils import to_camel


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

    rating_key: str | None = None
    key: str | None = None
    guid: str
    studio: str | None = None
    type: PlexMediaType
    title: str
    title_sort: str | None = None
    library_section_title: str | None = None
    library_sectionID: str | None = None
    library_section_key: str | None = None
    content_rating: str | None = None
    summary: str | None = None
    rating: float | None = None
    audience_rating: float | None = None
    year: int | None = None
    tagline: str | None = None
    thumb: str | None = None
    art: str | None = None
    duration: int | None = None
    originally_available_at: str | None = None
    added_at: int
    updated_at: int | None = None
    audience_rating_image: str | None = None
    has_premium_primary_extra: str | None = None
    rating_image: str | None = None
    media: list = Field(alias='Media', default_factory=list)
    genre: list = Field(alias='Genre', default_factory=list)
    country: list = Field(alias='Country', default_factory=list)
    guids: list = Field(alias='Guid', default_factory=list)
    ratings: list = Field(alias='Ratings', default_factory=list)
    director: list = Field(alias='Director', default_factory=list)
    writer: list = Field(alias='Writer', default_factory=list)
    role: list = Field(alias='Role', default_factory=list)
    producer: list = Field(alias='Producer', default_factory=list)

    def to_stremio_meta(self, configuration):
        from plexio.models import PLEX_TO_STREMIO_MEDIA_TYPE
        from plexio.models.stremio import StremioMeta

        return StremioMeta(
            id=self.guid,
            type=PLEX_TO_STREMIO_MEDIA_TYPE[self.type],
            name=self.title,
            releaseInfo=str(self.year),
            imdbRating=self.audience_rating,
            description=self.summary,
            poster=str(
                configuration.streaming_url
                / self.thumb[1:]
                % {'X-Plex-Token': configuration.access_token},
            ),
            background=str(
                configuration.streaming_url
                / (self.art or self.thumb)[1:]
                % {'X-Plex-Token': configuration.access_token},
            ),
            genres=[g['tag'] for g in self.genre],
        )


class PlexEpisodeMeta(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    rating_key: str
    key: str
    parent_rating_key: str
    grandparent_rating_key: str
    guid: str
    studio: str
    type: str
    title: str
    grandparent_key: str
    parent_key: str
    grandparent_title: str
    parent_title: str
    content_rating: str
    summary: str
    index: int
    parent_index: int
    year: int | None = None
    thumb: str | None = None
    art: str | None = None
    parent_thumb: str | None = None
    grandparent_thumb: str | None = None
    grandparent_art: str | None = None
    grandparent_theme: str | None = None
    duration: int | None = None
    originally_available_at: str | None = None
    added_at: int
    updated_at: int | None = None
    media: list = Field(default_factory=list)

    def to_stremio_video_meta(self, configuration):
        from plexio.models.stremio import StremioVideoMeta

        if self.originally_available_at:
            released = f'{self.originally_available_at}T00:00:00.000Z'
        else:
            released = datetime.fromtimestamp(self.added_at).strftime(
                '%Y-%m-%dT%H:%M:%S.%fZ'
            )

        return StremioVideoMeta(
            id=self.guid,
            title=self.title,
            released=released,
            thumbnail=str(
                configuration.streaming_url
                / self.thumb[1:]
                % {'X-Plex-Token': configuration.access_token},
            ),
            episode=self.index,
            season=self.parent_index,
            overview=self.summary,
        )
