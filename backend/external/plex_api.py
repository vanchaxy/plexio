from http import HTTPStatus

from aiohttp import ClientSession
from yarl import URL

from backend.models.plex import AuthPin, PlexServer, PlexUser
from backend.settings import settings

PLEX_API_URL = URL('https://plex.tv/api/v2/')


async def create_auth_pin(client: ClientSession) -> AuthPin:
    async with client.post(
        PLEX_API_URL / 'pins',
        data={
            'strong': 'true',
            'X-Plex-Product': settings.product_name,
            'X-Plex-Client-Identifier': settings.identifier,
        },
    ) as response:
        json = await response.json()
        return AuthPin(**json)


async def get_auth_token(client: ClientSession, auth_pin: AuthPin) -> str:
    async with client.get(
        PLEX_API_URL / f'pins/{auth_pin.id}',
        params={
            'code': auth_pin.code,
            'X-Plex-Client-Identifier': settings.identifier,
        },
    ) as response:
        json = await response.json()
        return json['authToken']


async def get_user(client: ClientSession, token: str) -> PlexUser | None:
    async with client.get(
        PLEX_API_URL / 'user',
        params={
            'X-Plex-Product': settings.product_name,
            'X-Plex-Client-Identifier': settings.identifier,
            'X-Plex-Token': token,
        },
    ) as response:
        if response.status != HTTPStatus.OK:
            return
        json = await response.json()
        return PlexUser(**json)


async def get_servers(client: ClientSession, token: str) -> list[PlexServer]:
    async with client.get(
        PLEX_API_URL / 'resources',
        params={
            'includeHttps': 1,
            'includeRelay': 1,
            'X-Plex-Token': token,
            'X-Plex-Client-Identifier': settings.identifier,
        },
    ) as response:
        json = await response.json()
        return [
            PlexServer(**server) for server in json if 'server' in server['provides']
        ]
