"""Soft glow effect (ambient glow / soft focus / edge haze) used by the Licyk style filter.

Ported from https://github.com/licyk/sd-webui-licyk-style-image
"""

from __future__ import annotations

import numpy as np
from PIL import Image, ImageFilter


def gaussian_blur(data: np.ndarray, radius: float) -> np.ndarray:
    """Apply Gaussian blur to a float RGB array in [0, 1]."""

    if radius <= 0:
        return data
    img = Image.fromarray(np.uint8(np.clip(data, 0, 1) * 255 + 0.5), "RGB")
    img = img.filter(ImageFilter.GaussianBlur(radius=radius))
    return np.asarray(img, dtype=np.float32) / 255


def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    """Hermite interpolation between ``edge0`` and ``edge1``."""

    t = np.clip((x - edge0) / max(edge1 - edge0, 1e-6), 0, 1)
    return t * t * (3 - 2 * t)


def screen(base: np.ndarray, blend: np.ndarray) -> np.ndarray:
    """Screen blend mode."""

    return 1 - (1 - base) * (1 - blend)


def soft_light(base: np.ndarray, blend: np.ndarray) -> np.ndarray:
    """Soft light blend mode (pegtop formula)."""

    return (1 - 2 * blend) * base * base + 2 * blend * base


def run(
    image: Image.Image,
    strength: float = 0.6,
    threshold: float = 0.6,
    radius: float = 3,
    color: tuple[int, int, int] = (255, 240, 220),
    soft_focus: float = 0.3,
    edge_softness: float = 0.2,
) -> Image.Image:
    """Add ambient glow, soft focus and edge haze; disabled when ``strength`` is 0.

    ``radius`` is a percentage of the image short side. The image mode
    (RGB / RGBA) is preserved.
    """

    if strength <= 0:
        return image

    alpha = image.getchannel("A") if image.mode in ("RGBA", "LA") else None
    base = np.asarray(image.convert("RGB"), dtype=np.float32) / 255
    height, width = base.shape[:2]
    blur_radius = min(width, height) * radius / 100

    # Ambient glow: blur highlights at multiple scales, then screen blend
    if blur_radius > 0:
        luminance = base @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
        mask = smoothstep(threshold - 0.1, threshold + 0.1, luminance)
        bright = base * mask[..., None]
        glow = (
            gaussian_blur(bright, blur_radius) * 0.5
            + gaussian_blur(bright, blur_radius * 2) * 0.3
            + gaussian_blur(bright, blur_radius * 4) * 0.2
        )
        glow = glow * (np.array(color, dtype=np.float32) / 255)
        base = screen(base, np.clip(glow * strength, 0, 1))

    blurred = None

    # Soft focus: soft light blend with the blurred image
    if soft_focus > 0 and blur_radius > 0:
        blurred = gaussian_blur(base, blur_radius)
        base = base + (soft_light(base, blurred) - base) * soft_focus

    # Edge haze: blend image edges into the blurred and lifted image
    if edge_softness > 0 and blur_radius > 0:
        if blurred is None:
            blurred = gaussian_blur(base, blur_radius)
        y, x = np.ogrid[0:height, 0:width]
        dist = np.sqrt(
            ((x - (width - 1) / 2) / (width / 2)) ** 2
            + ((y - (height - 1) / 2) / (height / 2)) ** 2
        ) / np.sqrt(2)
        edge_mask = (np.clip((dist - 0.5) / 0.5, 0, 1) ** 2 * edge_softness)[..., None]
        haze = screen(blurred, blurred * 0.3)
        base = base + (haze - base) * edge_mask

    result = Image.fromarray(np.uint8(np.clip(base, 0, 1) * 255 + 0.5), "RGB")
    if alpha is not None:
        result.putalpha(alpha)
    return result
