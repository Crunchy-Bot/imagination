import asyncio

import uvicorn
import os
import aiohttp
import typing
import requests

from base64 import standard_b64encode
from fastapi import FastAPI
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from functools import partial

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
async def create_news(ctx: NewsContext):
    await ensure_session()

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

    loop = asyncio.get_running_loop()
    start = perf_counter()
    out = await loop.run_in_executor(pool, cb)
    stop = perf_counter() - start

    buff = standard_b64encode(out.read()).decode('utf-8')

    payload = {
        "format": "png",
        "data": buff,
        "category": "news",
    }

    r = await session.post(
        "https://images.crunchy.gg/admin/create/image",
        json=payload,
        headers={"Authorization": API_KEY}
    )
    r.raise_for_status()

    data = (await r.json())['data']

    return ImageResponse(
        render=f"{BASE_IMAGE_URL}/news/{data['file_id']}",
        message=f"Success! Rendered in {stop * 1000}ms"
    )


@app.post("/create/release")
async def create_release(ctx: ReleaseContext):
    await ensure_session()

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
    loop = asyncio.get_running_loop()
    image = await loop.run_in_executor(pool, cb)
    stop = perf_counter() - start

    buff = standard_b64encode(image.read()).decode('utf-8')

    payload = {
        "format": "png",
        "data": buff,
        "category": "release",
    }

    r = await session.post(
        "https://images.crunchy.gg/admin/create/image",
        json=payload,
        headers={"Authorization": API_KEY}
    )
    r.raise_for_status()

    data = (await r.json())['data']

    file_id = data['file_id']
    url = f"{BASE_IMAGE_URL}/release/{file_id}"

    return ImageResponse(
        render=url,
        message=f"Success! Rendered in {stop * 1000}ms"
    )


@app.post("/create/profile")
def create_profile():
    return "yert"


if __name__ == '__main__':
    uvicorn.run("main:app", host=HOST, port=PORT)
