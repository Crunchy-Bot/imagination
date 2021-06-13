from render.utils import wrap_and_join
from render.canvas import (
    get_canvas,
    RGBA,
    CANVAS_SIZE,
    CANVAS_CRUNCHYROLL_COLOUR,
    CANVAS_WHITE,
    CANVAS_BASE_COLOUR,

    TextBold,
    ITextNormal,
    TextNormal, ITextSemibold,
)

from PIL import ImageDraw, Image
from io import BytesIO
from datetime import datetime

STAR_DELTA = 20


def render_news(
    title: str,
    summary: str,
    author: str,
    thumbnail: BytesIO,
    description: str,
    background_colour: RGBA = CANVAS_BASE_COLOUR,
    text_colour: RGBA = CANVAS_WHITE,
    border_colour: RGBA = CANVAS_CRUNCHYROLL_COLOUR,
) -> BytesIO:

    PADDING = 5
    img = get_canvas(colour=background_colour)

    # thumbnail
    thumbnail = Image.open(thumbnail)
    thumbnail = thumbnail.resize((180, 180))
    img.paste(thumbnail, (PADDING, PADDING))

    canvas = ImageDraw.Draw(img)

    # separator line
    canvas.line(
        (195 + PADDING, 15 + PADDING, 195 + PADDING, 165 + PADDING),
        fill=border_colour,
        width=3,
    )

    # title text
    font = TextBold(size=28)
    text = wrap_and_join(title, characters=40, max_lines=2)
    canvas.multiline_text(
        (207 + PADDING, 20 + PADDING),
        text,
        font=font,
        fill=text_colour,
    )
    _, y_offset = font.getsize_multiline(text)

    # summary text
    font = ITextNormal(size=23)
    fill = RGBA(text_colour.red, text_colour.green, text_colour.blue, 150)
    text = wrap_and_join(summary, characters=55, max_lines=2)
    canvas.text(
        (207 + PADDING, 40 + y_offset + PADDING),
        f"\"{text}\"",
        font=font,
        fill=fill,
    )

    # description text
    font = TextNormal(size=24)
    text = wrap_and_join(description, characters=65, max_lines=5)
    canvas.multiline_text(
        (0 + PADDING, 190 + PADDING),
        text,
        font=font,
        fill=text_colour,
    )

    # time and author
    size = 20
    h_adjust = 10
    font = ITextSemibold(size=size)
    w, h = font.getsize(author)
    canvas.text(
        (CANVAS_SIZE.width - w - PADDING, CANVAS_SIZE.height - h_adjust - h),
        author,
        fill=border_colour,
        font=font
    )
    font = ITextNormal(size=size)
    w2, _ = font.getsize("By")
    w_total = w + w2
    canvas.text((
        CANVAS_SIZE.width - w_total - 5 - PADDING, CANVAS_SIZE.height - h_adjust - h),
        "By",
        font=font,
    )

    ts = datetime.utcnow().strftime('%B, %d %Y %I:%M%p GMT')
    ts = f"{ts} - "
    font = TextNormal(size=size)
    w3, _ = font.getsize(ts)
    w_total = w + w2 + w3
    canvas.text(
        (CANVAS_SIZE.width - w_total - 10 - PADDING, CANVAS_SIZE.height - h_adjust - h),
        ts,
        font=font,
    )

    buffer = BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)

    return buffer


if __name__ == '__main__':
    with open("../resources/images/test.png", "rb") as file:
        buff = BytesIO()
        buff.write(file.read())

    img_ = render_news(
        title="Crunchyroll Adds Farewell, My Dear Cramer: First Touch Prequel Anime Film",
        summary="Premieres tonight 6/10 at 9PM PDT",
        author="Humberto Saabedra",
        thumbnail=buff,
        description="Crunchyroll is excited to announce the addition of the prequel film to the My Dear Cramer TV anime, Farewell, My Dear Cramer: First Touch. Read on for the details."
    )

    img_ = Image.open(img_, formats=["PNG"])
    img_.save("foo.png")
