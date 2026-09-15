from typing import Any

from PIL import Image
import cv2
import numpy as np


def fix_float(val: float, eps: float=1e-3) -> float:
    return float(val) - eps


def gaussian(img: np.ndarray, kernel: int, sigma: float) -> np.ndarray:
    return cv2.GaussianBlur(img, (kernel, kernel), sigma)


def dog_filter(img: np.ndarray, kernel: int=0, sigma: float=1.4, k_sigma: float=1.6, gamma: float=1) -> np.ndarray:
    g1 = gaussian(img, kernel, sigma)
    g2 = gaussian(img, kernel, sigma * k_sigma)
    return g1 - fix_float(gamma) * g2


def xdog(img: Image.Image, kernel: int, sigma: float, k_sigma: float, eps: float, phi: float, gamma: float, color: str, scale: bool=True) -> Image.Image:
    img = np.array(img)
    if color == "gray":
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    dog = dog_filter(img, kernel, sigma, k_sigma, gamma)
    dog = dog / dog.max()
    e = 1 + np.tanh(fix_float(phi) * (dog - fix_float(eps)))
    e[e >= 1] = 1

    if color == "gray":
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    if not scale:
        e[e < 1] = 0
    return Image.fromarray((e * 255).astype("uint8"))


def run(*args: Any) -> Image.Image:
    return xdog(*args)
