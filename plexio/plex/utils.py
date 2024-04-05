import asyncio
import json
from json import JSONDecodeError

from aiohttp import ClientConnectorError
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
            if response.status >= 400:
                raise HTTPException(
                    status_code=502,
                    detail='Received error from plex server',
                )
            response_bytes = await response.read()
            return json.loads(response_bytes.decode())
    except JSONDecodeError as e:
        with configure_scope() as scope:
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
