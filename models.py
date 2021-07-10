from typing import List
from enum import Enum
from pydantic import BaseModel
from pydantic.types import constr, conint


class ReleaseContext(BaseModel):
    title: constr(strip_whitespace=True, curtail_length=150)
    episode_title: constr(strip_whitespace=True, curtail_length=50) = ""
    episode: int
    rating: conint(ge=0)
    description: constr(strip_whitespace=True, curtail_length=300)
    thumbnail: str
    tags: List[constr(strip_whitespace=True, curtail_length=20)]


class NewsContext(BaseModel):
    title: constr(strip_whitespace=True, curtail_length=200)
    summary: constr(strip_whitespace=True, curtail_length=300)
    author: constr(strip_whitespace=True, curtail_length=50)
    brief: constr(strip_whitespace=True, curtail_length=300)
    thumbnail: str


class ProfileType(Enum):
    general = "general"
    mal = "mal"
    anilist = "anilist"


class GeneralProfile(BaseModel):
    watchlist_count: conint(ge=0)
    favourites_count: conint(ge=0)
    collected_characters: conint(ge=0)


class ProfileContext(BaseModel):
    ...


class ImageResponse(BaseModel):
    render: str
    message: str
