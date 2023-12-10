from plexio.settings import settings


async def get_json(client, url, params=None):
    if params is None:
        params = {}
    async with client.get(
        url,
        params=params,
        timeout=settings.plex_requests_timeout,
    ) as response:
        json = await response.json()
        return json
