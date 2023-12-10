from contextlib import asynccontextmanager

import aiohttp
import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from plexio.routers.addon import router as addon_router
from plexio.routers.auth import router as auth_router
from plexio.routers.configuration import router as configuration_router
from plexio.settings import settings

sentry_sdk.init()


@asynccontextmanager
async def lifespan(app: FastAPI):
    plex_client = aiohttp.ClientSession(
        headers={'accept': 'application/json'},
    )
    redis_client = Redis(host=settings.redis_host)

    yield {
        'plex_client': plex_client,
        'redis_client': redis_client,
    }

    await plex_client.close()
    await redis_client.close()


app = FastAPI(
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=settings.cors_origin_regex,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(addon_router)
app.include_router(auth_router)
app.include_router(configuration_router)
