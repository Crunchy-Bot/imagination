from render.utils import wrap_and_join
from render.canvas import (
    get_canvas,
    CANVAS_CRUNCHYROLL_COLOUR,
    CANVAS_SIZE,
    CANVAS_GRAY_300,
    STAR,
    TextSemibold,
    ITextNormal,
)

from PIL import ImageDraw, Image
from io import BytesIO
from textwrap import shorten

STAR_DELTA = 20


def render_release(
    title: str,
    stars: int,
    thumbnail: BytesIO,
    description: str,
) -> BytesIO:
    img = get_canvas()

    # title adjustments
    font = TextSemibold(size=20)
    max_width = int(CANVAS_SIZE.width * 0.90)
    w, _ = font.getsize(title)
    avg_width_per_char = w / len(title)
    width = int((max_width - 100) / avg_width_per_char)
    title_text = shorten(title, width=width)
    w, h = font.getsize_multiline(title_text)

    canvas = ImageDraw.Draw(img)
    canvas.multiline_text((20, 15), title_text, font=font)

    # title border
    canvas.line(
        (20, 24 + h, 20 + w, 24 + h),
        fill=CANVAS_CRUNCHYROLL_COLOUR,
        width=2,
    )

    # stars
    star = STAR
    for i in range(1, stars + 1):
        img.paste(star, (CANVAS_SIZE.width - (STAR_DELTA * i) - 20, 15))

    # thumbnail
    thumb = Image.open(thumbnail)
    thumb = thumb.resize((188, 256))
    img.paste(thumb, (20, h + 40))

    # desc
    font = ITextNormal(size=16)
    w, _ = font.getsize(description)
    avg_width_per_char = w / len(description)
    width = int((max_width - 200) / avg_width_per_char)
    description = wrap_and_join(description, width, max_lines=14)
    canvas.multiline_text(
        (20 + 188 + 20, h + 40),
        description,
        fill=CANVAS_GRAY_300,
        font=font,
    )

    buffer = BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)

    return buffer


if __name__ == '__main__':
    with open("../resources/images/fb.jpg", "rb") as file:
        buff = BytesIO()
        buff.write(file.read())

    img_ = render_release(
        title="{{ title }} Episode {{ episode }}",
        stars=4,
        thumbnail=buff,
        description="After some discussion with Mark in the comments on my first answer, I decided to make another solution using OpenCV and NumPy, which is able to easily feed some real images, e.g. photos, to the method and get the image including a border with rounded corners, and transparency outside the border!",
    )

