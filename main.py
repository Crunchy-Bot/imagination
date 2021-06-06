import asyncio

import uvicorn
import os
import aiohttp
import typing

from base64 import standard_b64encode
from io import BytesIO
from fastapi import FastAPI
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from render.release import render_release
from render.news import render_news
from models import *

BASE_IMAGE_URL = "https://images.crunchy.gg/content"
API_KEY = os.getenv("IMAGE_API_KEY")

pool = ThreadPoolExecutor()
session: typing.Optional[aiohttp.ClientSession] = None
app = FastAPI(
    title="Crunchy Image Render",
    version="0.1.0",
    docs_url=None,
    redoc_url="/"
)


async def ensure_session():
    global session
    if session is None:
        session = aiohttp.ClientSession()


@app.post(
    "/create/news",
    response_model=ImageResponse,
    description="Creates a news image with the provided payload.",
)
async def create_news(payload: NewsContext):
    await ensure_session()

    r = await session.get(payload.thumbnail)
    r.raise_for_status()

    buff = BytesIO()
    buff.write(await r.read())

    cb = partial(
        render_news,
        title=payload.title,
        summary=payload.summary,
        author=payload.author,
        thumbnail=buff,
        description=payload.brief,
    )

    start = perf_counter()
    loop = asyncio.get_running_loop()
    image = await loop.run_in_executor(pool, cb)
    stop = perf_counter() - start

    buff = standard_b64encode(image.read()).decode('utf-8')

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

    file_id = data['file_id']
    url = f"{BASE_IMAGE_URL}/news/{file_id}"

    return ImageResponse(
        url=url,
        message=f"Success! Rendered in {stop * 1000}ms"
    )


@app.post("/create/release")
async def create_release(payload: ReleaseContext):
    await ensure_session()

    r = await session.get(payload.thumbnail)
    r.raise_for_status()

    buff = BytesIO()
    buff.write(await r.read())

    cb = partial(
        render_release,
        title=payload.title,
        stars=payload.stars,
        thumbnail=buff,
        description=payload.description,
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
        url=url,
        message=f"Success! Rendered in {stop * 1000}ms"
    )


@app.post("/create/profile")
def create_profile():
    return "yert"


if __name__ == '__main__':
    uvicorn.run("main:app")
