from typing import List, Tuple
from render.canvas import (
    CANVAS_BASE_COLOUR,
    CANVAS_WHITE,
    CANVAS_CRUNCHYROLL_COLOUR,
)
from enum import Enum
from pydantic import BaseModel
from pydantic.types import constr, conint


ColourLimit = conint(ge=0, le=255)
_RGBA = Tuple[ColourLimit, ColourLimit, ColourLimit, ColourLimit]


class Colours(BaseModel):
    background_colour: _RGBA = tuple(CANVAS_BASE_COLOUR)
    text_colour: _RGBA = tuple(CANVAS_WHITE)
    border_colour: _RGBA = tuple(CANVAS_CRUNCHYROLL_COLOUR)


COLOURS_DEFAULT = Colours()


class ReleaseContext(BaseModel):
    title: constr(strip_whitespace=True, curtail_length=150)
    episode_title: constr(strip_whitespace=True, curtail_length=50)
    episode: int
    rating: conint(ge=0)
    description: constr(strip_whitespace=True, curtail_length=300)
    thumbnail: str
    tags: List[constr(strip_whitespace=True, curtail_length=20)]
    colours: Colours = COLOURS_DEFAULT


class NewsContext(BaseModel):
    title: constr(strip_whitespace=True, curtail_length=200)
    summary: constr(strip_whitespace=True, curtail_length=300)
    author: constr(strip_whitespace=True, curtail_length=50)
    brief: constr(strip_whitespace=True, curtail_length=300)
    thumbnail: str
    colours: Colours = COLOURS_DEFAULT


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
