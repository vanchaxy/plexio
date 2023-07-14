import base64
import json
from typing import Annotated

from aiohttp import ClientSession
from fastapi import Cookie, Depends, HTTPException, Request, status
from redis.asyncio.client import Redis
from sentry_sdk import set_user

from backend.external.plex_api import get_user
from backend.models.addon import AddonConfiguration


def get_http_client(request: Request) -> ClientSession:
    return request.state.plex_client


def get_redis_client(request: Request) -> Redis:
    return request.state.redis_client


async def get_plex_auth_token(
    http: Annotated[ClientSession, Depends(get_http_client)],
    plex_auth_token: Annotated[str | None, Cookie()] = None,
) -> str:
    if plex_auth_token is not None:
        user = await get_user(http, plex_auth_token)
        if user:
            return plex_auth_token
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def get_addon_configuration(base64_cfg: str | None = None) -> AddonConfiguration | None:
    if base64_cfg is None:
        return
    decoded = base64.b64decode(base64_cfg)
    configuration = AddonConfiguration(**json.loads(decoded))
    set_user({'id': configuration.installation_id})
    return configuration
