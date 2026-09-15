"""Combined noise and chromatic aberration effect."""

from __future__ import annotations

from PIL import Image

from .chromatic import run as run_chromatic
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
) -> Image.Image:
    """Apply the original Licyk style processing order."""

    image = run_noise(
        image=image,
        noise_level=noise_strength,
        noise_color=(noise_r, noise_g, noise_b),
        opacity=opacity,
        offset_percentage=offset_percentage,
        seed=seed,
    )
    return run_chromatic(
        image.convert("RGB"),
        chromatic_strength,
        chromatic_blur,
    )
