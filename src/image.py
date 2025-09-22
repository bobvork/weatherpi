import os
from PIL import Image, ImageDraw, ImageFont
from weer import get_weather

#
# Source for icons: https://erikflowers.github.io/weather-icons/
#


def icon_for_weather(weather):
    # print(f"icon for {weather}")
    mapping = {
        "zonnig": "",
        "bliksem": "",
        "regen": "",
        "buien": "",
        "hagel": "",
        "mist": "",
        "sneeuw": "",
        "bewolkt": "",
        "lichtbewolkt": "",
        "halfbewolkt": "",
        "halfbewolkt_regen": "",
        "zwaarbewolkt": "",
        "nachtmist": "",
        "helderenacht": "",
        "nachtbewolkt": "",
        "wolkennacht": "",
    }
    return mapping[weather] if weather in mapping else "?"


def draw_line(draw, x1, y1, x2, y2, w, h):
    draw.line((x1 * h, y1 * w, x2 * h, y2 * w), fill=0)


def create_image(width, height, assets_dir):
    font_xs = ImageFont.truetype(
        os.path.join(assets_dir, "opensans-condensedmedium.ttf"), 13
    )
    font_sm = ImageFont.truetype(os.path.join(assets_dir, "opensans-medium.ttf"), 20)
    font_md = ImageFont.truetype(
        os.path.join(assets_dir, "opensans-condensedmedium.ttf"), 27
    )
    font_lg = ImageFont.truetype(
        os.path.join(assets_dir, "opensans-condensedmedium.ttf"), 36
    )
    icon_font = ImageFont.truetype(os.path.join(assets_dir, "weathericons.ttf"), 48)
    icon_sm = ImageFont.truetype(os.path.join(assets_dir, "weathericons.ttf"), 28)
    DrawImage = Image.new("1", (height, width), 255)
    draw = ImageDraw.Draw(DrawImage)

    weather = get_weather()
    draw.text(
        (height - 4, 4),
        f"{weather.update_date}",
        font=font_xs,
        fill=0,
        align="right",
        anchor="rt",
    )
    draw.text((20, 10), icon_for_weather(weather.icon), font=icon_font, fill=0)
    draw.text((80, 20), f"{weather.current_temp} °", font=font_lg, fill=0)

    draw.text((20, 70), f"Regen: {weather.rain_percent}%", font=font_sm, fill=0)

    draw.text(
        (210, 20),
        f"{weather.max_temp}°\n{weather.min_temp}°",
        font=font_md,
        fill=0,
        align="right",
    )

    draw.text(
        (190, 20),
        "",
        font=icon_sm,
        fill=0,
        align="right",
    )
    draw.text(
        (190, 52),
        "",
        font=icon_sm,
        fill=0,
        align="right",
    )
    # draw.text((170, 50), f"L: {weather.min_temp} °C", font=font_md, fill=0)

    draw_line(draw, 0.05, 0.66, 0.95, 0.66, width, height)

    draw.text((10, 127), "", font=icon_sm, fill=0)

    draw.text(
        (65, 128),
        f"{weather.tomorrow_min} - {weather.tomorrow_max}°",
        font=font_md,
        fill=0,
    )

    draw.text((170, 127), "", font=icon_sm, fill=0)

    draw.text(
        (210, 128),
        f"{weather.tomorrow_rain}%",
        font=font_md,
        fill=0,
    )
    return DrawImage
