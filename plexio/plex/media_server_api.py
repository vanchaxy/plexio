import asyncio
from http import HTTPStatus

from aiohttp import ClientConnectorError, ClientSession
from redis.asyncio.client import Redis
from yarl import URL

from plexio.models.plex import (
    PlexEpisodeMeta,
    PlexLibrarySection,
    PlexMediaMeta,
    PlexMediaType,
)
from plexio.plex.utils import get_json
from plexio.settings import settings

TYPE_TO_DUMMY_ID = {}


async def check_server_connection(
    *,
    client: ClientSession,
    url: URL,
    token: str,
) -> bool:
    try:
        async with client.get(
            url,
            params={
                'X-Plex-Token': token,
            },
            timeout=settings.plex_requests_timeout,
        ) as response:
            if response.status != HTTPStatus.OK:
                return False
            return True
    except (asyncio.TimeoutError, ClientConnectorError):
        return False


async def get_sections(
    *,
    client: ClientSession,
    url: URL,
    token: str,
) -> list[PlexLibrarySection]:
    json = await get_json(
        client=client,
        url=url / 'library/sections',
        params={
            'X-Plex-Token': token,
        },
    )
    return [
        PlexLibrarySection(**section)
        for section in json['MediaContainer']['Directory']
        if section['type'] in {PlexMediaType.movie, PlexMediaType.show}
    ]


async def get_section_media(
    *,
    client: ClientSession,
    url: URL,
    token: str,
    section_id: str,
    skip: int,
    search: str,
) -> list[PlexMediaMeta]:
    params = {
        'includeGuids': 1,
        'X-Plex-Container-Start': skip,
        'X-Plex-Container-Size': 100,
        'X-Plex-Token': token,
    }
    if search:
        params['title'] = search
    json = await get_json(
        client=client,
        url=url / 'library/sections' / section_id / 'all',
        params=params,
    )
    metadata = json['MediaContainer'].get('Metadata', [])
    return [PlexMediaMeta(**meta) for meta in metadata]


async def get_media(
    *,
    client: ClientSession,
    url: URL,
    token: str,
    guid: str,
    get_only_first=False,
) -> list[PlexMediaMeta]:
    json = await get_json(
        client=client,
        url=url / 'library/all',
        params={
            'guid': guid,
            'X-Plex-Token': token,
        },
    )
    media_sections = json['MediaContainer'].get('Metadata', [])
    media_metas = []
    for section in media_sections:
        json = await get_json(
            client=client,
            url=url / 'library/metadata' / section['ratingKey'],
            params={
                'X-Plex-Token': token,
                'includeElements': 'Stream',
            },
        )
        metadata = json['MediaContainer']['Metadata'][0]
        media_metas.append(PlexMediaMeta(**metadata))
        if get_only_first:
            break
    return media_metas


async def get_all_episodes(
    *,
    client: ClientSession,
    url: URL,
    token: str,
    key: str,
) -> list[PlexEpisodeMeta]:
    json = await get_json(
        client=client,
        url=str(url / key[1:]).replace('/children', '/allLeaves'),
        params={
            'X-Plex-Token': token,
        },
    )
    metadata = json['MediaContainer'].get('Metadata', [])
    return [PlexEpisodeMeta(**meta) for meta in metadata]


async def get_dummy_media_id(*, client: ClientSession, media_type: PlexMediaType):
    if dummy_id := TYPE_TO_DUMMY_ID.get(media_type):
        return dummy_id
    json = await get_json(
        client=client,
        url=settings.matching_plex_address / 'library/all',
    )
    metadata = json.get('MediaContainer', {}).get('Metadata', [])
    for meta in metadata:
        if meta['type'] == media_type:
            TYPE_TO_DUMMY_ID[media_type] = meta['ratingKey']
            return meta['ratingKey']


async def imdb_to_plex_id(
    *,
    client: ClientSession,
    imdb_id: str,
    media_type: PlexMediaType,
) -> str:
    dummy_media_id = await get_dummy_media_id(
        client=client,
        media_type=media_type,
    )
    json = await get_json(
        client=client,
        url=settings.matching_plex_address
        / f'library/metadata/{dummy_media_id}/matches',
        params={
            'manual': 1,
            'title': f'imdb-{imdb_id}',
        },
    )
    guid = json['MediaContainer']['SearchResult'][0]['guid']
    return guid


async def get_episode_guid(
    *,
    client: ClientSession,
    url: URL,
    token: str,
    show_guid: str,
    season: str,
    episode: str,
) -> str:
    all_episodes = await get_all_episodes(
        client=client,
        url=url,
        token=token,
        key=show_guid,
    )
    for metadata in all_episodes:
        if str(metadata.parent_index) == season and str(metadata.index) == episode:
            return metadata.guid


async def stremio_to_plex_id(
    *,
    client: ClientSession,
    url: URL,
    token: str,
    redis: Redis,
    stremio_id: str,
    media_type: PlexMediaType,
) -> str | None:
    if cached_plex_id := await redis.get(stremio_id):
        return cached_plex_id.decode()

    if media_type == PlexMediaType.show:
        imdb_id, season, episode = stremio_id.split(':')
    else:
        imdb_id = stremio_id

    plex_id = await imdb_to_plex_id(
        client=client,
        imdb_id=imdb_id,
        media_type=media_type,
    )

    if media_type == PlexMediaType.show:
        media = await get_media(
            client=client,
            url=url,
            token=token,
            guid=plex_id,
        )
        for meta in media:
            plex_id = await get_episode_guid(
                client=client,
                url=url,
                token=token,
                show_guid=meta.key,
                season=season,
                episode=episode,
            )
            if plex_id:
                break

    if plex_id:
        await redis.set(imdb_id, plex_id)
    return plex_id
