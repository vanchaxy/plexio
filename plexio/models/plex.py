import os
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from plexio.models.utils import get_flag_emoji, to_camel


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

    guid: str
    type: PlexMediaType
    title: str
    added_at: int

    rating_key: str | None = None
    key: str | None = None
    studio: str | None = None
    title_sort: str | None = None
    library_section_title: str | None = None
    library_sectionID: str | None = None
    library_section_key: str | None = None
    content_rating: str | None = None
    summary: str = ''
    rating: float | None = None
    audience_rating: float | None = None
    year: int | None = None
    tagline: str | None = None
    thumb: str | None = None
    art: str | None = None
    duration: int | None = None
    originally_available_at: str | None = None
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

    def get_year(self):
        if self.year:
            return str(self.year)
        return datetime.fromtimestamp(self.added_at).strftime('%Y')

    def to_stremio_meta(self, configuration):
        from plexio.models import PLEX_TO_STREMIO_MEDIA_TYPE
        from plexio.models.stremio import StremioMeta

        return StremioMeta(
            id=self.guid,
            type=PLEX_TO_STREMIO_MEDIA_TYPE[self.type],
            name=self.title,
            releaseInfo=self.get_year(),
            imdbRating=self.audience_rating,
            description=self.summary,
            poster=str(
                configuration.streaming_url
                / self.thumb[1:]
                % {'X-Plex-Token': configuration.access_token},
            )
            if self.thumb
            else None,
            background=str(
                configuration.streaming_url
                / (self.art or self.thumb)[1:]
                % {'X-Plex-Token': configuration.access_token},
            )
            if (self.art or self.thumb)
            else None,
            genres=[g['tag'] for g in self.genre],
        )

    def to_stremio_meta_review(self, configuration):
        from plexio.models import PLEX_TO_STREMIO_MEDIA_TYPE
        from plexio.models.stremio import StremioMetaPreview

        imdb_id = None
        guids = self.guids
        for guid in guids:
            if guid['id'].startswith('imdb://'):
                imdb_id = guid['id'][7:]

        return StremioMetaPreview(
            id=imdb_id or self.guid,
            name=self.title,
            releaseInfo=str(self.year),
            poster=str(
                configuration.streaming_url
                / self.thumb[1:]
                % {'X-Plex-Token': configuration.access_token},
            )
            if self.thumb
            else None,
            type=PLEX_TO_STREMIO_MEDIA_TYPE[self.type],
            imdbRating=self.audience_rating,
            description=self.summary,
            genres=[g['tag'] for g in self.genre],
        )

    def get_stremio_streams(self, configuration):
        from plexio.models.stremio import StremioStream

        streams = []
        for i, media in enumerate(self.media):
            name = f'{configuration.server_name} {self.library_section_title}'
            filename = os.path.basename(media['Part'][0]['file'])

            audio_languages = set()
            subtitles_languages = set()
            for part_stream in media['Part'][0].get('Stream', []):
                if part_stream['streamType'] == 2:
                    audio_languages.add(
                        get_flag_emoji(part_stream.get('languageTag', 'Unknown'))
                    )
                elif part_stream['streamType'] == 3:
                    subtitles_languages.add(
                        get_flag_emoji(part_stream.get('languageTag', 'Unknown'))
                    )

            description_template = (
                f'{filename}\n'
                f'{{quality}}\n'
                f'{"/".join(sorted(audio_languages))} '
                f'({"/".join(sorted(subtitles_languages))})'
            )
            quality_description = f'Direct Play {media["videoResolution"]}'
            streams.append(
                StremioStream(
                    name=name,
                    description=description_template.format(
                        quality=quality_description
                    ),
                    url=str(
                        configuration.streaming_url
                        / media['Part'][0]['key'][1:]
                        % {
                            'X-Plex-Token': configuration.access_token,
                        },
                    ),
                    behaviorHints={'bingeGroup': quality_description},
                )
            )

            transcode_url = (
                configuration.streaming_url
                / 'video/:/transcode/universal/start.m3u8'
                % {
                    'path': self.key,
                    'mediaIndex': i,
                    'protocol': 'hls',
                    'fastSeek': 1,
                    'copyts': 1,
                    'autoAdjustQuality': 0,
                    'X-Plex-Platform': 'Chrome',
                    'X-Plex-Token': configuration.access_token,
                }
            )

            quality_description = f'Transcode {media["videoResolution"]} (original)'
            streams.append(
                StremioStream(
                    name=name,
                    description=description_template.format(
                        quality=quality_description
                    ),
                    url=str(transcode_url % {'videoQuality': 100}),
                    behaviorHints={'bingeGroup': quality_description},
                )
            )

            for quality in configuration.qualities:
                if media['width'] <= quality['min_width']:
                    continue
                quality_description = f'Transcode {quality["name"]}'
                streams.append(
                    StremioStream(
                        name=name,
                        description=description_template.format(
                            quality=quality_description
                        ),
                        url=str(transcode_url % quality['plex_args']),
                        behaviorHints={'bingeGroup': quality_description},
                    )
                )

        return streams


class PlexEpisodeMeta(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    guid: str
    title: str
    index: int
    parent_index: int
    added_at: int

    type: str | None = None
    rating_key: str | None = None
    key: str | None = None
    parent_rating_key: str | None = None
    grandparent_rating_key: str | None = None
    studio: str | None = None
    grandparent_key: str | None = None
    parent_key: str | None = None
    grandparent_title: str | None = None
    parent_title: str | None = None
    content_rating: str | None = None
    summary: str = ''
    year: int | None = None
    thumb: str | None = None
    art: str | None = None
    parent_thumb: str | None = None
    grandparent_thumb: str | None = None
    grandparent_art: str | None = None
    grandparent_theme: str | None = None
    duration: int | None = None
    originally_available_at: str | None = None
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
            )
            if self.thumb
            else None,
            episode=self.index,
            season=self.parent_index,
            overview=self.summary,
        )
