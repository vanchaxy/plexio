from typing import Annotated

from aiohttp import ClientSession
from fastapi import APIRouter, Depends
from yarl import URL

from plexio.dependencies import get_http_client
from plexio.plex.media_server_api import check_server_connection

router = APIRouter(prefix='/api/v1')


@router.get('/test-connection')
async def test_connection(
    http: Annotated[ClientSession, Depends(get_http_client)],
    url: str,
    token: str,
):
    success = await check_server_connection(
        client=http,
        url=URL(url),
        token=token,
    )
    return {'success': success}
