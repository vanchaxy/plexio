from typing import Annotated

from aiohttp import ClientSession
from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio.client import Redis

from plexio.dependencies import (
    get_addon_configuration,
    get_http_client,
    get_redis_client,
)
from plexio.external.plex_media_server import (
    get_all_episodes,
    get_media,
    get_section_media,
    get_sections,
    stremio_to_plex_id,
)
from plexio.models import PLEX_TO_STREMIO_MEDIA_TYPE, STREMIO_TO_PLEX_MEDIA_TYPE
from plexio.models.addon import AddonConfiguration
from plexio.models.stremio import (
    StremioCatalog,
    StremioCatalogManifest,
    StremioManifest,
    StremioMediaType,
    StremioMetaPreview,
    StremioMetaResponse,
    StremioStream,
    StremioStreamsResponse,
)

router = APIRouter()


@router.get('/manifest.json')
@router.get('/{base64_cfg}/manifest.json')
async def get_manifest(
    http: Annotated[ClientSession, Depends(get_http_client)],
    configuration: Annotated[
        AddonConfiguration | None,
        Depends(get_addon_configuration),
    ],
) -> StremioManifest:
    catalogs = []
    description = 'Play movies and series from plex.tv.'
    name = 'Plexio'

    if configuration is not None:
        sections = await get_sections(
            client=http,
            url=configuration.discovery_url,
            token=configuration.access_token,
        )

        for section in sections:
            catalogs.append(
                StremioCatalogManifest(
                    id=section.key,
                    type=PLEX_TO_STREMIO_MEDIA_TYPE[section.type],
                    name=f'{section.title} | {configuration.server_name}',
                    extra=[
                        {'name': 'skip', 'isRequired': False},
                        {'name': 'search', 'isRequired': False},
                    ],
                ),
            )

        name += f' ({configuration.server_name})'
        description += f' Your installation ID: {configuration.installation_id}'

    return StremioManifest(
        id='com.stremio.plexio',
        version='0.0.1',
        description=description,
        name=name,
        resources=[
            'stream',
            'catalog',
            {
                'name': 'meta',
                'types': ['movie', 'series'],
                'idPrefixes': ['plex://', 'local://'],
            },
        ],
        types=[StremioMediaType.movie, StremioMediaType.series],
        catalogs=catalogs,
        idPrefixes=['tt', 'plex://', 'local://'],
        behaviorHints={
            'configurable': True,
            'configurationRequired': configuration is None,
        },
        contactEmail='support@plexio.stream',
    )


@router.get('/{base64_cfg}/catalog/{stremio_type}/{catalog_id}.json')
@router.get('/{base64_cfg}/catalog/{stremio_type}/{catalog_id}/skip={skip}.json')
@router.get('/{base64_cfg}/catalog/{stremio_type}/{catalog_id}/search={search}.json')
async def get_catalog(
    http: Annotated[ClientSession, Depends(get_http_client)],
    configuration: Annotated[AddonConfiguration, Depends(get_addon_configuration)],
    stremio_type: StremioMediaType,
    catalog_id: str,
    skip: int = 0,
    search: str = '',
) -> StremioCatalog:
    media = await get_section_media(
        client=http,
        url=configuration.discovery_url,
        token=configuration.access_token,
        section_id=catalog_id,
        search=search,
        skip=skip,
    )

    metas = []
    for meta in media:
        imdb_id = None
        guids = meta.guids
        for guid in guids:
            if guid['id'].startswith('imdb://'):
                imdb_id = guid['id'][7:]

        meta_preview = StremioMetaPreview(
            id=imdb_id or meta.guid,
            name=meta.title,
            releaseInfo=str(meta.year),
            poster=str(
                configuration.streaming_url
                / meta.thumb[1:]
                % {'X-Plex-Token': configuration.access_token},
            ),
            type=PLEX_TO_STREMIO_MEDIA_TYPE[meta.type],
            imdbRating=meta.audience_rating,
            description=meta.summary,
            genres=[g['tag'] for g in meta.genres],
        )
        metas.append(meta_preview)

    return StremioCatalog(metas=metas)


@router.get('/{base64_cfg}/meta/{stremio_type}/{plex_id:path}.json')
async def get_meta(
    http: Annotated[ClientSession, Depends(get_http_client)],
    configuration: Annotated[AddonConfiguration, Depends(get_addon_configuration)],
    stremio_type: StremioMediaType,
    plex_id: str,
) -> StremioMetaResponse:
    media = await get_media(
        client=http,
        url=configuration.discovery_url,
        token=configuration.access_token,
        guid=plex_id,
    )
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    media = media[0]

    meta = media.to_stremio_meta(configuration)

    if stremio_type == StremioMediaType.series:
        episodes = await get_all_episodes(
            client=http,
            url=configuration.discovery_url,
            token=configuration.access_token,
            key=media.key,
        )
        videos = []
        for episode in episodes:
            videos.append(episode.to_stremio_video_meta(configuration))
        meta.videos = videos
    return StremioMetaResponse(meta=meta)


@router.get('/{base64_cfg}/stream/{stremio_type}/{media_id:path}.json')
async def get_stream(
    http: Annotated[ClientSession, Depends(get_http_client)],
    redis: Annotated[Redis, Depends(get_redis_client)],
    configuration: Annotated[AddonConfiguration, Depends(get_addon_configuration)],
    stremio_type: StremioMediaType,
    media_id: str,
) -> StremioStreamsResponse:
    if media_id.startswith('tt'):
        plex_id = await stremio_to_plex_id(
            client=http,
            url=configuration.discovery_url,
            token=configuration.access_token,
            redis=redis,
            stremio_id=media_id,
            media_type=STREMIO_TO_PLEX_MEDIA_TYPE[stremio_type],
        )
        if not plex_id:
            return StremioStreamsResponse()
    else:
        plex_id = media_id

    media = await get_media(
        client=http,
        url=configuration.discovery_url,
        token=configuration.access_token,
        guid=plex_id,
    )
    return StremioStreamsResponse(
        streams=[
            StremioStream(
                name=f'{configuration.server_name} {meta.section}',
                title=f'{meta.title}\n{meta.year}',
                url=str(
                    configuration.streaming_url
                    / 'video/:/transcode/universal/start.m3u8'
                    % {
                        'path': meta.key,
                        'mediaIndex': 0,
                        'partIndex': 0,
                        'protocol': 'hls',
                        'fastSeek': 1,
                        'copyts': 1,
                        'offset': 0,
                        'X-Plex-Platform': 'Chrome',
                        'X-Plex-Token': configuration.access_token,
                    },
                ),
                behavior_hints={},
            )
            for meta in media
        ],
    )
