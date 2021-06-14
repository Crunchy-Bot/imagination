import asyncio

import uvicorn
import os
import aiohttp
import typing
import requests

from base64 import standard_b64encode
from io import BytesIO
from fastapi import FastAPI
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from render.canvas import RGBA
from render.release import render_release
from render.news import render_news
from models import *

BASE_IMAGE_URL = "https://images.crunchy.gg/content"
API_KEY = os.getenv("IMAGE_API_KEY")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 5000))


pool = ThreadPoolExecutor(max_workers=10)
session: typing.Optional[aiohttp.ClientSession] = None
app = FastAPI(
    title="Crunchy Image Render",
    version="0.1.0",
    docs_url=None,
    redoc_url="/"
)


def run_callback_then_submit(cb) -> str:
    buff = cb()
    buff = standard_b64encode(buff.read()).decode('utf-8')

    payload = {
        "format": "png",
        "data": buff,
        "category": "news",
    }

    r = requests.post(
        "https://images.crunchy.gg/admin/create/image",
        json=payload,
        headers={"Authorization": API_KEY}
    )
    r.raise_for_status()

    data = r.json()['data']

    return data['file_id']


async def ensure_session():
    global session
    if session is None:
        session = aiohttp.ClientSession()


@app.post(
    "/create/news",
    response_model=ImageResponse,
    description="Creates a news image with the provided payload.",
)
async def create_news(payload: NewsItems):
    await ensure_session()

    ctx = payload.ctx
    r = await session.get(ctx.thumbnail)
    r.raise_for_status()
    buff = await r.read()

    cb = partial(
        render_news,
        title=ctx.title,
        summary=ctx.summary,
        author=ctx.author,
        thumbnail=buff,
        description=ctx.brief,
    )

    start = perf_counter()
    tasks = {}
    loop = asyncio.get_running_loop()

    for colour_set in payload.items:
        caller = partial(
            cb,
            background_colour=RGBA(*colour_set.colours.background_colour),
            text_colour=RGBA(*colour_set.colours.text_colour),
            border_colour=RGBA(*colour_set.colours.border_colour),
        )
        t = loop.run_in_executor(pool, run_callback_then_submit, caller)
        tasks[colour_set.id] = t
    await asyncio.gather(*tasks.values())
    stop = perf_counter() - start

    urls = {
        id_: f"{BASE_IMAGE_URL}/news/{await fut}"
        for id_, fut in tasks.items()
    }

    return ImageResponse(
        renders=urls,
        message=f"Success! Rendered in {stop * 1000}ms"
    )


@app.post("/create/release")
async def create_release(payload: ReleaseItems):
    await ensure_session()

    ctx = payload.ctx
    r = await session.get(ctx.thumbnail)
    r.raise_for_status()
    buff = await r.read()

    cb = partial(
        render_release,
        title=ctx.title,
        episode_title=ctx.episode_title,
        episode=ctx.episode,
        rating=ctx.rating,
        tags=ctx.tags,
        thumbnail=buff,
        description=ctx.description,
    )

    start = perf_counter()
    tasks = {}
    loop = asyncio.get_running_loop()

    for colour_set in payload.items:
        caller = partial(
            cb,
            background_colour=RGBA(*colour_set.colours.background_colour),
            text_colour=RGBA(*colour_set.colours.text_colour),
            border_colour=RGBA(*colour_set.colours.border_colour),
        )
        t = loop.run_in_executor(pool, run_callback_then_submit, caller)
        tasks[colour_set.id] = t
    await asyncio.gather(*tasks.values())
    stop = perf_counter() - start

    urls = {
        id_: f"{BASE_IMAGE_URL}/release/{await fut}"
        for id_, fut in tasks.items()
    }

    return ImageResponse(
        renders=urls,
        message=f"Success! Rendered in {stop * 1000}ms"
    )


@app.post("/create/profile")
def create_profile():
    return "yert"


if __name__ == '__main__':
    uvicorn.run("main:app", host=HOST, port=PORT)
