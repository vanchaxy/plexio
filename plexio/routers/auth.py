from typing import Annotated

from aiohttp import ClientSession
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from yarl import URL

from plexio.dependencies import get_http_client, get_plex_auth_token
from plexio.external.plex_api import create_auth_pin, get_auth_token, get_user
from plexio.models.plex import AuthPin, PlexUser
from plexio.settings import settings

router = APIRouter(prefix='/api/v1')


@router.get('/login')
async def login(
    request: Request,
    http: Annotated[ClientSession, Depends(get_http_client)],
    origin_url: str = '/',
) -> RedirectResponse:
    auth_pin = await create_auth_pin(http)

    forward_url = URL(
        str(request.url_for('auth_redirect')),
    ) % {
        'code': auth_pin.code,
        'id': auth_pin.id,
        'origin_url': origin_url,
    }

    redirect_url = URL('https://app.plex.tv/auth')
    redirect_url = redirect_url % {
        'code': auth_pin.code,
        'forwardUrl': str(forward_url),
        'clientID': settings.identifier,
    }

    redirect_url = str(redirect_url).replace('/auth?', '/auth#?')
    return RedirectResponse(redirect_url)


@router.get('/logout')
async def logout() -> RedirectResponse:
    response = RedirectResponse('/')
    response.set_cookie(key='plex_auth_token', value='', max_age=1)
    return response


@router.get('/auth-redirect')
async def auth_redirect(
    http: Annotated[ClientSession, Depends(get_http_client)],
    auth_pin: Annotated[AuthPin, Depends()],
    origin_url: str,
) -> RedirectResponse:
    auth_token = await get_auth_token(http, auth_pin)
    response = RedirectResponse(origin_url)
    response.set_cookie(key='plex_auth_token', value=auth_token)
    return response


@router.get('/get-plex-user')
async def get_plex_user(
    http: Annotated[ClientSession, Depends(get_http_client)],
    plex_auth_token: Annotated[str, Depends(get_plex_auth_token)],
) -> PlexUser:
    plex_user = await get_user(http, plex_auth_token)
    return plex_user
