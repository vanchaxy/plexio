import json
from json import JSONDecodeError

from aiohttp import ClientConnectorError, ServerDisconnectedError
from fastapi import HTTPException
from sentry_sdk import configure_scope

from plexio.settings import settings


class PlexUnauthorizedError(BaseException):
    pass


async def get_json(client, url, params=None):
    if params is None:
        params = {}
    try:
        async with client.get(
            url,
            params=params,
            timeout=settings.plex_requests_timeout,
        ) as response:
            # log unauthorized to sentry
            if response.status in (401, 403):
                raise PlexUnauthorizedError
            if response.status >= 400:
                raise HTTPException(
                    status_code=502,
                    detail='Received error from plex server',
                )
            response_bytes = await response.read()
            return json.loads(response_bytes.decode(errors='ignore'))
    except JSONDecodeError as e:
        with configure_scope() as scope:
            scope.add_attachment(bytes=response_bytes, filename='attachment.txt')
            raise e
    except ClientConnectorError as e:
        raise HTTPException(
            status_code=502,
            detail='Plex server connection error',
        ) from e
    except ServerDisconnectedError as e:
        raise HTTPException(
            status_code=502,
            detail='Plex server disconnected error',
        ) from e
    except TimeoutError as e:
        raise HTTPException(
            status_code=504,
            detail='Plex server timeout error',
        ) from e
