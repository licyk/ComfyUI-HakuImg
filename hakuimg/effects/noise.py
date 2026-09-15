"""Noise overlay effect used by the Licyk style filter."""

from __future__ import annotations

import numpy as np
from PIL import Image


def run(
    image: Image.Image,
    noise_level: float = 0.4,
    noise_color: tuple[int, int, int] = (255, 255, 255),
    opacity: int = 128,
    offset_percentage: int = 20,
    seed: int = 0,
) -> Image.Image:
    """Overlay randomly distributed, color-shifted noise on an image."""

    base_image = image.convert("RGBA")
    if noise_level <= 0 or opacity <= 0:
        return base_image

    width, height = base_image.size

    rng = np.random.default_rng(seed)
    noise_mask = rng.random((height, width)) < noise_level
    max_offset = int(255 * (offset_percentage / 100))
    offsets = rng.integers(
        -max_offset,
        max_offset + 1,
        size=(height, width, 3),
        dtype=np.int16,
    )
    colors = np.asarray(noise_color, dtype=np.int16) + offsets
    colors = np.clip(colors, 0, 255).astype(np.uint8)

    noise_data = np.zeros((height, width, 4), dtype=np.uint8)
    noise_data[:, :, :3] = colors
    noise_data[:, :, 3] = np.where(noise_mask, opacity, 0).astype(np.uint8)
    noise_layer = Image.fromarray(noise_data, mode="RGBA")

    return Image.alpha_composite(base_image, noise_layer)
