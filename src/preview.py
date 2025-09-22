#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import os

from image import create_image

DISP_WIDTH = 176
DISP_HEIGHT = 264

assets_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pic")
logging.basicConfig(level=logging.INFO)


def my_image():
    DrawImage = create_image(DISP_WIDTH, DISP_HEIGHT, assets_dir)
    DrawImage.save("preview.png")


if __name__ == "__main__":
    my_image()
