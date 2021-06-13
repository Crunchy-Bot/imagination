from typing import List
from enum import Enum
from pydantic import BaseModel
from pydantic.types import constr, conint


class ReleaseContext(BaseModel):
    title: constr(strip_whitespace=True, curtail_length=150)
    episode: int
    stars: conint(ge=0)
    description: constr(strip_whitespace=True, curtail_length=300)
    thumbnail: str


class NewsContext(BaseModel):
    title: constr(strip_whitespace=True, curtail_length=200)
    summary: constr(strip_whitespace=True, curtail_length=300)
    author: constr(strip_whitespace=True, curtail_length=50)
    brief: constr(strip_whitespace=True, curtail_length=300)
    thumbnail: str

    class Config:
        schema_extra = {
            "example": {
                "title": "FEATURE: It's Hime's Birthday! Here's Some Of Her Top Anime Recs",
                "summary": "It's Crunchyroll-Hime's birthday, let's celebrate with these awesome anime",
                "author": "Brianna Albert",
                "brief": "It's Hime's birthday! From Tokyo Revengers to So I'm A Spider, So What, here are some recs that'll keep you on your feet!",
                "thumbnail": "https://img1.ak.crunchyroll.com/i/spire4/b65773eead0332e03d11e82a44a5e3771622768400_thumb.jpg"
            }
        }


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
    url: str
    message: str
