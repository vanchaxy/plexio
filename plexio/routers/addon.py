from itertools import chain
from typing import Annotated

from aiohttp import ClientSession
from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio.client import Redis

from plexio import __version__
from plexio.dependencies import (
    get_addon_configuration,
    get_cache,
    get_http_client,
)
from plexio.models import PLEX_TO_STREMIO_MEDIA_TYPE, STREMIO_TO_PLEX_MEDIA_TYPE
from plexio.models.addon import AddonConfiguration
from plexio.models.stremio import (
    StremioCatalog,
    StremioCatalogManifest,
    StremioManifest,
    StremioMediaType,
    StremioMetaResponse,
    StremioStreamsResponse,
)
from plexio.plex.media_server_api import (
    get_all_episodes,
    get_media,
    get_section_media,
    get_sections,
    stremio_to_plex_id,
)

router = APIRouter()


@router.get('/manifest.json', response_model_exclude_none=True)
@router.get('/{base64_cfg}/manifest.json', response_model_exclude_none=True)
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
        version=__version__,
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


@router.get(
    '/{base64_cfg}/catalog/{stremio_type}/{catalog_id}.json',
    response_model_exclude_none=True,
)
@router.get(
    '/{base64_cfg}/catalog/{stremio_type}/{catalog_id}/skip={skip}.json',
    response_model_exclude_none=True,
)
@router.get(
    '/{base64_cfg}/catalog/{stremio_type}/{catalog_id}/search={search}.json',
    response_model_exclude_none=True,
)
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
    return StremioCatalog(
        metas=[m.to_stremio_meta_review(configuration) for m in media]
    )


@router.get(
    '/{base64_cfg}/meta/{stremio_type}/{plex_id:path}.json',
    response_model_exclude_none=True,
)
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
        get_only_first=True,
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
        meta.videos = [e.to_stremio_video_meta(configuration) for e in episodes]
    return StremioMetaResponse(meta=meta)


@router.get(
    '/{base64_cfg}/stream/{stremio_type}/{media_id:path}.json',
    response_model_exclude_none=True,
)
async def get_stream(
    http: Annotated[ClientSession, Depends(get_http_client)],
    cache: Annotated[Redis, Depends(get_cache)],
    configuration: Annotated[AddonConfiguration, Depends(get_addon_configuration)],
    stremio_type: StremioMediaType,
    media_id: str,
) -> StremioStreamsResponse:
    if media_id.startswith('tt'):
        plex_id = await stremio_to_plex_id(
            client=http,
            url=configuration.discovery_url,
            token=configuration.access_token,
            cache=cache,
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
        streams=chain.from_iterable(
            meta.get_stremio_streams(configuration) for meta in media
        ),
    )
