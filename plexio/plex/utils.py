import asyncio

from aiohttp import ClientConnectorError, ContentTypeError
from fastapi import HTTPException
from sentry_sdk import configure_scope

from plexio.settings import settings


async def get_json(client, url, params=None):
    if params is None:
        params = {}
    try:
        async with client.get(
            url,
            params=params,
            timeout=settings.plex_requests_timeout,
        ) as response:
            json = await response.json()
            return json
    except ContentTypeError as e:
        with configure_scope() as scope:
            response_bytes = await response.read()
            scope.add_attachment(bytes=response_bytes, filename='attachment.txt')
            raise e
    except ClientConnectorError as e:
        raise HTTPException(
            status_code=502,
            detail='Plex server connection error',
        ) from e
    except asyncio.TimeoutError as e:
        raise HTTPException(
            status_code=504,
            detail='Plex server timeout error',
        ) from e
