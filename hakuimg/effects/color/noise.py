import numpy as np
from PIL import ImageChops, Image


def get_noise(img: Image.Image, value: float) -> Image.Image:
    if value <= 0:
        return img

    noise = np.random.randint(0, value * 100, img.size, np.uint8)
    noise_img = Image.fromarray(noise, "L").resize(img.size).convert(img.mode)
    return ImageChops.add(img, noise_img)
