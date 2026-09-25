"""Combined glow, noise and chromatic aberration effect."""

from __future__ import annotations

import numpy as np
from PIL import Image

from .chromatic import run as run_chromatic
from .glow import run as run_glow
from .noise import run as run_noise


def run(
    image: Image.Image,
    noise_strength: float,
    noise_r: int,
    noise_g: int,
    noise_b: int,
    opacity: int,
    chromatic_strength: float,
    chromatic_blur: bool,
    offset_percentage: int,
    seed: int,
    glow_strength: float = 0,
    glow_threshold: float = 0.6,
    glow_radius: float = 3,
    glow_r: int = 255,
    glow_g: int = 240,
    glow_b: int = 220,
    glow_soft_focus: float = 0.3,
    glow_edge_softness: float = 0.2,
) -> Image.Image:
    """Apply the original Licyk style processing order."""

    image = run_glow(
        image,
        strength=glow_strength,
        threshold=glow_threshold,
        radius=glow_radius,
        color=(glow_r, glow_g, glow_b),
        soft_focus=glow_soft_focus,
        edge_softness=glow_edge_softness,
    )
    image = run_noise(
        image=image,
        noise_level=noise_strength,
        noise_color=(noise_r, noise_g, noise_b),
        opacity=opacity,
        offset_percentage=offset_percentage,
        seed=seed,
    ).convert("RGB")

    size = image.size
    image = run_chromatic(image, chromatic_strength, chromatic_blur)
    # Chromatic aberration crops to odd dimensions; restore the original size
    # by repeating edge pixels.
    if image.size != size:
        data = np.asarray(image)
        pad = ((0, size[1] - image.size[1]), (0, size[0] - image.size[0]), (0, 0))
        image = Image.fromarray(np.pad(data, pad, mode="edge"), image.mode)
    return image
