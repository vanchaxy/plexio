import base64
import json

from aiohttp import ClientSession
from fastapi import Request
from sentry_sdk import set_user

from plexio.models.addon import AddonConfiguration


def get_http_client(request: Request) -> ClientSession:
    return request.state.plex_client


def get_cache(request: Request):
    return request.state.cache


def get_addon_configuration(base64_cfg: str | None = None) -> AddonConfiguration | None:
    if base64_cfg is None:
        return None
    decoded = base64.b64decode(base64_cfg)
    configuration = AddonConfiguration(**json.loads(decoded))
    return configuration


def set_sentry_user(installation_id: str | None = None) -> None:
    if installation_id:
        set_user({'id': installation_id})
