from aiohttp import ContentTypeError
from sentry_sdk import configure_scope

from plexio.settings import settings


async def get_json(client, url, params=None):
    if params is None:
        params = {}
    async with client.get(
        url,
        params=params,
        timeout=settings.plex_requests_timeout,
    ) as response:
        try:
            json = await response.json()
        except ContentTypeError as e:
            with configure_scope() as scope:
                response_bytes = await response.read()
                scope.add_attachment(bytes=response_bytes, filename='attachment.txt')
                raise e
        return json
