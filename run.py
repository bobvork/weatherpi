#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import os
import sys
import time

from PIL import Image, ImageDraw, ImageFont
from image import create_image
from weer import get_weather

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pic")
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in7_V2

logging.basicConfig(level=logging.INFO)


def init():
    logging.info("init and Clear")
    epd.init()
    epd.Clear()


def stop():
    init()
    logging.info("Goto Sleep...")
    epd.sleep()


try:
    logging.info("Starting...")
    epd = epd2in7_V2.EPD()
    init()

    DrawImage = create_image(epd.width, epd.height, picdir)
    epd.display(epd.getbuffer(DrawImage))
    time.sleep(5)

    epd2in7_V2.epdconfig.module_exit(cleanup=True)
    stop()


except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in7_V2.epdconfig.module_exit(cleanup=True)
    exit()
