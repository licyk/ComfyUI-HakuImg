from typing import Any

from PIL import Image, ImageFilter


def run(img: Image.Image, img_blur: float) -> Image.Image:
    blur = ImageFilter.GaussianBlur(img_blur)
    return img.filter(blur)
