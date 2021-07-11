import numpy as np

from PIL import Image, ImageFont
from collections import namedtuple
from functools import partial

CanvasSpec = namedtuple("CanvasSpec", ["width", "height"])
RGBA = namedtuple("RGB", ["red", "green", "blue", "alpha"])

CANVAS_SIZE = CanvasSpec(760, 400)
CANVAS_BASE_COLOUR = RGBA(47, 49, 54, 255)
CANVAS_CRUNCHYROLL_COLOUR = RGBA(232, 126, 21, 255)
CANVAS_FUNIMATION_COLOUR = RGBA(255, 255, 255, 255)
CANVAS_CRUNCHYROLL_BRIGHT_COLOUR = RGBA(255, 153, 0, 255)
CANVAS_WHITE = RGBA(255, 255, 255, 255)
CANVAS_GRAY_300 = RGBA(209, 213, 219, 255)
CANVAS_GRAY_400 = RGBA(156, 163, 175, 255)
CANVAS_GRAY_700 = RGBA(55, 65, 81, 255)

RESOURCES_FOLDER = "./resources/"

STAR: Image.Image = Image.open(f"{RESOURCES_FOLDER}/images/star.png")
_BaseFont = partial(ImageFont.truetype)

# Standard
TextNormal = partial(_BaseFont, f"{RESOURCES_FOLDER}/Arial/Roboto-Regular.ttf")
TextSemibold = partial(_BaseFont, f"{RESOURCES_FOLDER}/Arial/Roboto-Medium.ttf")
TextBold = partial(_BaseFont, f"{RESOURCES_FOLDER}/Arial/Roboto-Bold.ttf")

# Italics
ITextNormal = partial(_BaseFont, f"{RESOURCES_FOLDER}/Arial/Roboto-Italic.ttf")
ITextSemibold = partial(_BaseFont, f"{RESOURCES_FOLDER}/Arial/Roboto-MediumItalic.ttf")
ITextBold = partial(_BaseFont, f"{RESOURCES_FOLDER}/Arial/Roboto-BoldItalic.ttf")


def get_canvas(colour: RGBA = CANVAS_BASE_COLOUR) -> Image.Image:
    """ creates a canvas with the constant defaults """
    return Image.new("RGBA", CANVAS_SIZE, color=colour)


def get_star(colour: RGBA = CANVAS_CRUNCHYROLL_COLOUR, background: RGBA = CANVAS_BASE_COLOUR) -> Image.Image:
    data = np.array(STAR)  # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

    blank_areas = (red == 0) & (green == 0) & (blue == 0) & (alpha == 0)
    data[...][blank_areas.T] = background  # Transpose back needed

    orange_blank = (red == 255) & (green == 172) & (blue == 51)
    data[..., :-1][orange_blank.T] = (colour.red, colour.green, colour.blue)  # Transpose back needed

    return Image.fromarray(data).resize((20, 20))
