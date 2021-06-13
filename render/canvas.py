from PIL import Image, ImageFont
from collections import namedtuple
from functools import partial


CanvasSpec = namedtuple("CanvasSpec", ["width", "height"])
RGBA = namedtuple("RGB", ["red", "green", "blue", "alpha"])

CANVAS_SIZE = CanvasSpec(760, 400)
CANVAS_BASE_COLOUR = RGBA(47, 49, 54, 255)
CANVAS_CRUNCHYROLL_COLOUR = RGBA(232, 126, 21, 255)
CANVAS_CRUNCHYROLL_BRIGHT_COLOUR = RGBA(255, 153, 0, 255)
CANVAS_WHITE = RGBA(255, 255, 255, 255)
CANVAS_GRAY_300 = RGBA(209, 213, 219, 255)
CANVAS_GRAY_400 = RGBA(156, 163, 175, 255)
CANVAS_GRAY_700 = RGBA(55, 65, 81, 255)

RESOURCES_FOLDER = "../resources/"

STAR: Image.Image = Image.open(f"{RESOURCES_FOLDER}/images/star.png").resize((20, 20))

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

