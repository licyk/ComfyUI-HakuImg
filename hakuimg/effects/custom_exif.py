from PIL import Image


def run(img: Image.Image, text: str) -> Image.Image:
    if not text:
        return img

    img.info["parameters"] = text
    return img
