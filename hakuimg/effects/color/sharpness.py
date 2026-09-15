from PIL import ImageEnhance, Image


def get_sharpness(img: Image.Image, value: float) -> Image.Image:
    if value <= 0:
        return img

    return ImageEnhance.Sharpness(img).enhance((value + 1) * 1.5)
