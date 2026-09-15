from __future__ import annotations
from typing import Any


import numpy as np
import cv2
from PIL import Image


def resize_with_mask(
    img: Image.Image, w: int, h: int, t: int, b: int, l: int, r: int,
) -> tuple[Image.Image, Image.Image]:
    new_img = Image.new("RGB", (w, h))
    new_img.paste(img, (l, t))

    mask = Image.new("L", (w, h), 255)
    mask_none = Image.new("L", (r-l, b-t), 0)
    mask.paste(mask_none, (l, t))
    return new_img, mask
