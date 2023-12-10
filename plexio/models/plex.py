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

    key: str
    guid: str
    type: PlexMediaType
    title: str
    year: int | None = None
    summary: str
    thumb: str | None = None
    art: str | None = None
    section: str | None = Field(alias='librarySectionTitle', default=None)
    guids: list = Field(alias='Guid', default_factory=list)
    audience_rating: float | None = None
    originally_available_at: str | None = None
    added_at: int | None = None
    updated_at: int | None = None
    duration: int | None = None
    genres: list = Field(alias='Genre', default_factory=list)
    countries: list = Field(alias='Country', default_factory=list)
    directors: list = Field(alias='Director', default_factory=list)
    writers: list = Field(alias='Writer', default_factory=list)
    cast: list = Field(alias='Role', default_factory=list)

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
            genres=[g['tag'] for g in self.genres],
        )


class PlexEpisodeMeta(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    guid: str
    title: str
    originally_available_at: str | None = None
    thumb: str | None = None
    episode: int = Field(alias='index')
    season: int = Field(alias='parentIndex')
    summary: str

    def to_stremio_video_meta(self, configuration):
        from plexio.models.stremio import StremioVideoMeta

        return StremioVideoMeta(
            id=self.guid,
            title=self.title,
            released=f'{self.originally_available_at}T00:00:00.000Z',
            thumbnail=str(
                configuration.streaming_url
                / self.thumb[1:]
                % {'X-Plex-Token': configuration.access_token},
            ),
            episode=self.episode,
            season=self.season,
            overview=self.summary,
        )
