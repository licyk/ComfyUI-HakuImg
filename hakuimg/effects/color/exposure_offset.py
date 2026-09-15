from typing import Any

from PIL import ImageEnhance, Image
import numpy as np


def get_exposure_offset(img: Image.Image, value: float, brightness_value: float) -> Image.Image:
    if value <= 0:
        return img

    np_img = np.array(img).astype(float) + value * 75
    np_img = np.clip(np_img, 0, 255).astype(np.uint8)
    img = Image.fromarray(np_img)
    return ImageEnhance.Brightness(img).enhance((brightness_value + 1) - value / 4)
