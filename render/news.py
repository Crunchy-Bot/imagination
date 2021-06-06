from render.utils import wrap_and_join
from render.canvas import (
    get_canvas,
    CANVAS_CRUNCHYROLL_COLOUR,
    CANVAS_SIZE,
    CANVAS_GRAY_300,
    CANVAS_GRAY_400,
    CANVAS_GRAY_700,
    TextSemibold,
    TextNormal,
    ITextNormal,
    ITextSemibold,
)

from PIL import ImageDraw, Image
from io import BytesIO
from textwrap import shorten
from datetime import datetime

STAR_DELTA = 20


def render_news(
    title: str,
    summary: str,
    author: str,
    thumbnail: BytesIO,
    description: str,
) -> BytesIO:
    img = get_canvas()

    # title adjustments
    max_width = int(CANVAS_SIZE.width * 0.90)
    w, _ = TextSemibold(size=20).getsize(title)
    avg_width_per_char = w / len(title)
    width = int(max_width / avg_width_per_char)
    title_text = shorten(title, width=width)
    w, h = TextSemibold(size=20).getsize_multiline(title_text)

    canvas = ImageDraw.Draw(img)
    canvas.multiline_text((20, 15), title_text, font=TextSemibold(size=20))

    # title border
    canvas.line(
        (20, 22 + h, 20 + w, 22 + h),
        fill=CANVAS_CRUNCHYROLL_COLOUR,
        width=2,
    )

    # summary
    font = ITextNormal(size=16)
    summary = f"\"{summary}"
    w, _ = font.getsize(summary)
    avg_width_per_char = w / len(summary)
    width = int(max_width / avg_width_per_char)
    summary = wrap_and_join(summary, width)
    canvas.multiline_text((20, h + 35), f"{summary}\"", fill=CANVAS_GRAY_400, font=font)

    # thumbnail
    thumb = Image.open(thumbnail)
    thumb = thumb.resize((188, 188))
    img.paste(thumb, (20, CANVAS_SIZE.height - 208))

    # desc
    w, _ = ITextNormal(size=16).getsize(description)
    avg_width_per_char = w / len(description)
    width = int((max_width - 200) / avg_width_per_char)
    description = wrap_and_join(description, width, max_lines=12)
    canvas.multiline_text(
        (20 + 188 + 20, CANVAS_SIZE.height - 208),
        description,
        fill=CANVAS_GRAY_300,
        font=ITextNormal(size=16),
    )

    # separation line
    canvas.line(
        (20, CANVAS_SIZE.height - 220, CANVAS_SIZE.width - 20, CANVAS_SIZE.height - 220),
        fill=CANVAS_GRAY_700,
        width=2,
    )

    # author and time
    ts = datetime.utcnow().strftime('%B, %d %Y %I:%M%p GMT')
    ts = f"{ts} - "
    font = TextNormal(size=14)
    w, _ = font.getsize(ts)
    canvas.text((20, CANVAS_SIZE.height - 245), ts, font=font)

    font = ITextNormal(size=14)
    w2, _ = font.getsize("By")
    canvas.text((20 + w + 5, CANVAS_SIZE.height - 245), "By", font=font)

    font = ITextSemibold(size=14)
    canvas.text(
        (20 + w + w2 + 10, CANVAS_SIZE.height - 245),
        author,
        fill=CANVAS_CRUNCHYROLL_COLOUR,
        font=font
    )

    buffer = BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)

    return buffer


if __name__ == '__main__':
    with open("../resources/images/news.png", "rb") as file:
        buff = BytesIO()
        buff.write(file.read())

    img_ = render_news(
        title="FEATURE: It's Hime's Birthday! Here's Some Of Her Top Anime Recs",
        summary="Registered to the new Crunchyroll site on June 15",
        author="Daryl Harding",
        thumbnail=buff,
        description="After some discussion with Mark in the comments on my first answer, I decided to make another solution using OpenCV and NumPy, which is able to easily feed some real images, e.g. photos, to the method and get the image including a border with rounded corners, and transparency outside the border! new website experience by default. Hit the jump to read more about the new Crunchyroll website experience!"
    )