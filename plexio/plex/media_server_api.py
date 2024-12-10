from http import HTTPStatus

from aiohttp import ClientConnectorError, ClientSession
from yarl import URL

from plexio.models.plex import (
    PlexEpisodeMeta,
    PlexMediaMeta,
    PlexMediaType,
)
from plexio.plex.utils import get_json
from plexio.settings import settings

PLEX_CACHE_TTL = 24 * 60 * 60

SORT_OPTIONS = {
    'Title': 'title',
    'Title (desc)': 'title:desc',
    'Year': 'year',
    'Year (desc)': 'year:desc',
    'Release Date': 'originallyAvailableAt',
    'Release Date (desc)': 'originallyAvailableAt:desc',
    'Critic Rating': 'rating',
    'Critic Rating (desc)': 'rating:desc',
    'Audience Rating': 'audienceRating',
    'Audience Rating (desc)': 'audienceRating:desc',
    'Rating': 'userRating',
    'Rating (desc)': 'userRating:desc',
    'Content Rating': 'contentRating',
    'Content Rating (desc)': 'contentRating:desc',
    'Duration': 'duration',
    'Duration (desc)': 'duration:desc',
    'Progress': 'viewOffset',
    'Progress (desc)': 'viewOffset:desc',
    'Plays': 'viewCount',
    'Plays (desc)': 'viewCount:desc',
    'Date Added': 'addedAt',
    'Date Added (desc)': 'addedAt:desc',
    'Date Viewed': 'lastViewedAt',
    'Date Viewed (desc)': 'lastViewedAt:desc',
    'ResolutionSelected': 'mediaHeight',
    'ResolutionSelected (desc)': 'mediaHeight:desc',
    'Bitrate': 'mediaBitrate',
    'Bitrate (desc)': 'mediaBitrate:desc',
    'Randomly': 'random',
}


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
    except (TimeoutError, ClientConnectorError):
        return False


async def get_section_media(
    *,
    client: ClientSession,
    url: URL,
    token: str,
    section_id: str,
    skip: int,
    search: str,
    sort: str,
) -> list[PlexMediaMeta]:
    params = {
        'includeGuids': 1,
        'X-Plex-Container-Start': skip,
        'X-Plex-Container-Size': 100,
        'X-Plex-Token': token,
    }
    if search:
        params['title'] = search
    if sort:
        params['sort'] = SORT_OPTIONS[sort]
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
        if section['type'] not in ('show', 'movie', 'episode'):
            continue
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
    episodes = []
    for i, meta in enumerate(metadata):
        meta.setdefault('index', i)
        episodes.append(PlexEpisodeMeta(**meta))
    return episodes


async def imdb_to_plex_id(
    *,
    client: ClientSession,
    imdb_id: str,
    media_type: PlexMediaType,
    token: str,
) -> str:
    json = await get_json(
        client=client,
        url='https://metadata.provider.plex.tv/library/metadata/matches',
        params={
            'X-Plex-Token': settings.plex_matching_token or token,
            'type': 1 if media_type is PlexMediaType.movie else 2,
            'title': f'imdb-{imdb_id}',
            'guid': f'com.plexapp.agents.imdb://{imdb_id}?lang=en',
        },
    )
    media_container = json['MediaContainer']
    if media_container['totalSize']:
        return media_container['Metadata'][0]['guid']


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
    cache,
    stremio_id: str,
    media_type: PlexMediaType,
) -> str | None:
    if cached_plex_id := await cache.get(stremio_id):
        return cached_plex_id

    if media_type == PlexMediaType.show:
        id_season_episode = stremio_id.split(':')
        if len(id_season_episode) != 3:
            return None
        imdb_id, season, episode = id_season_episode
    else:
        imdb_id = stremio_id

    plex_id = await imdb_to_plex_id(
        client=client,
        imdb_id=imdb_id,
        media_type=media_type,
        token=token,
    )
    if not plex_id:
        return None

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
        else:
            return None

    if plex_id:
        await cache.set(stremio_id, plex_id, ex=PLEX_CACHE_TTL)
    return plex_id
