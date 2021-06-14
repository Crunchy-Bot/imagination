from render.utils import wrap_and_join
from render.canvas import (
    get_canvas,
    CANVAS_CRUNCHYROLL_COLOUR,
    CANVAS_SIZE,
    CANVAS_GRAY_300,
    STAR,
    TextSemibold,
    ITextNormal,
    ITextSemibold,
    RGBA,
    CANVAS_BASE_COLOUR,
    CANVAS_WHITE, TextBold, get_star, TextNormal,
)

from PIL import ImageDraw, Image
from io import BytesIO
from typing import List
from datetime import datetime

STAR_DELTA = 20


def render_release(
    title: str,
    episode_title: str,
    episode: int,
    rating: int,
    tags: List[str],
    thumbnail: bytes,
    description: str,
    background_colour: RGBA = CANVAS_BASE_COLOUR,
    text_colour: RGBA = CANVAS_WHITE,
    border_colour: RGBA = CANVAS_CRUNCHYROLL_COLOUR,
) -> BytesIO:
    PADDING = 5
    img = get_canvas(colour=background_colour)

    # thumbnail
    thumbnail = BytesIO(thumbnail)
    thumbnail = Image.open(thumbnail)
    thumbnail = thumbnail.resize((228, 342))
    img.paste(thumbnail, (PADDING, PADDING))

    # separator line
    canvas = ImageDraw.Draw(img)
    canvas.line(
        (243 + PADDING, 15 + PADDING, 243 + PADDING, 327),
        fill=border_colour,
        width=3,
    )

    X_ALIGN = 258 + PADDING  # +10px from line

    # title text
    font = TextBold(size=24)
    text = wrap_and_join(title, characters=45, max_lines=2)
    canvas.multiline_text(
        (X_ALIGN, 20 + PADDING),
        text,
        font=font,
        fill=text_colour,
    )
    _, y_offset = font.getsize_multiline(text)

    # episode number and title
    y = 40 + PADDING + y_offset
    font = TextBold(size=20)
    episode_render_text = f"Episode {episode} - "
    canvas.text(
        (X_ALIGN, y),
        episode_render_text,
        fill=text_colour,
        font=font,
    )
    x_offset, _ = font.getsize_multiline(episode_render_text)

    font = ITextSemibold(size=20)
    fill = RGBA(text_colour.red, text_colour.green, text_colour.blue, 150)
    canvas.text(
        (X_ALIGN + x_offset + 2, y),  # +2px for padding correction
        f"\"{episode_title}\"",
        fill=fill,
        font=font,
    )

    # rating
    y = y + 30
    font = TextBold(size=20)
    text = "Rating"
    canvas.text(
        (X_ALIGN, y),
        text,
        fill=text_colour,
        font=font,
    )
    x_offset, _ = font.getsize_multiline(text)
    star = get_star(border_colour, background_colour)

    for _ in range(rating):
        img.paste(
            star,
            (X_ALIGN + x_offset + 5, y + 2),
        )
        x_offset += 22

    # tags
    y = y + 30
    font = TextBold(size=20)
    text = "Tags - "
    canvas.text(
        (X_ALIGN, y),
        text,
        fill=text_colour,
        font=font,
    )
    x_offset, _ = font.getsize_multiline(text)

    font = ITextSemibold(size=18)
    fill = RGBA(text_colour.red, text_colour.green, text_colour.blue, 150)
    canvas.text(
        (X_ALIGN + x_offset + 2, y + 2),  # +2px for padding correction
        ", ".join(tags),
        fill=fill,
        font=font,
    )

    # description
    y = y + 40
    font = ITextNormal(size=20)
    fill = RGBA(text_colour.red, text_colour.green, text_colour.blue, 120)
    description = wrap_and_join(description, characters=50, max_lines=5)
    canvas.multiline_text(
        (X_ALIGN, y),
        description,
        fill=fill,
        font=font,
    )

    # time and author
    size = 18
    h_adjust = 30

    ts = datetime.utcnow().strftime('%B, %d %Y %I:%M%p GMT')
    font = TextNormal(size=size)
    w, _ = font.getsize(ts)
    canvas.text(
        (CANVAS_SIZE.width - w - 10 - PADDING, CANVAS_SIZE.height - h_adjust),
        ts,
        font=font,
    )

    buffer = BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)

    return buffer


if __name__ == '__main__':
    with open("../resources/images/thumb.jpg", "rb") as file:
        buff = BytesIO()
        buff.write(file.read())

    img_ = render_release(
        title="Higehiro: After Being Rejected, I Shaved and Took in a High School Runaway",
        episode_title="Hello, world",
        episode=10,
        rating=5,
        tags=["drama", "foo", "bar"],
        thumbnail=buff,
        description="After some discussion with Mark in the comments on my first answer, I decided to make another solution using OpenCV and NumPy, which is able to easily feed some real images, e.g. photos, to the method and get the image including a border with rounded corners, and transparency outside the border!",
    )

    img_ = Image.open(img_, formats=["PNG"])
    img_.save("foo.png")
