from PIL import Image, ImageFont
from collections import namedtuple
from functools import partial


CanvasSpec = namedtuple("CanvasSpec", ["width", "height"])
RGB = namedtuple("RGB", ["red", "green", "blue"])

CANVAS_SIZE = CanvasSpec(700, 344)
CANVAS_BASE_COLOUR = RGB(17, 24, 39)
CANVAS_CRUNCHYROLL_COLOUR = RGB(232, 126, 21)
CANVAS_CRUNCHYROLL_BRIGHT_COLOUR = RGB(255, 153, 0)
CANVAS_WHITE = RGB(255, 255, 255)
CANVAS_GRAY_300 = RGB(209, 213, 219)
CANVAS_GRAY_400 = RGB(156, 163, 175)
CANVAS_GRAY_700 = RGB(55, 65, 81)

RESOURCES_FOLDER = "./resources/"

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


def get_canvas() -> Image.Image:
    """ creates a canvas with the constant defaults """
    return Image.new("RGB", CANVAS_SIZE, color=CANVAS_BASE_COLOUR)

