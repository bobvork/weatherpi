import os
from PIL import Image, ImageDraw, ImageFont
from weer import get_weather


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

    print("Drawing text and line")

    weather = get_weather()
    draw.text((10, 10), icon_for_weather(weather.icon), font=icon_font, fill=0)
    draw.text((70, 20), f"{weather.current_temp} °", font=font_lg, fill=0)

    draw.text((10, 70), f"Regen: {weather.rain_percent}%", font=font_sm, fill=0)

    draw.text((170, 20), f"H: {weather.max_temp} °C", font=font_md, fill=0)
    draw.text((170, 50), f"L: {weather.min_temp} °C", font=font_md, fill=0)

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
