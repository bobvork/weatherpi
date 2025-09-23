#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import os
import sys


picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pic")
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in7_V2

logging.basicConfig(level=logging.INFO)


try:
    logging.info("Starting...")
    epd = epd2in7_V2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()
    epd2in7_V2.epdconfig.module_exit(cleanup=True)


except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in7_V2.epdconfig.module_exit(cleanup=True)
    exit()
