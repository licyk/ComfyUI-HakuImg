import torch
import numpy as np
from PIL import Image
from ..hakuimg.neon import run


class NEON:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "glow_mode": (
                    [
                        "BS",
                        "BMBL"
                    ],
                ),
                "blur": (
                    "INT", {
                        "default": 16,
                        "min": 2,
                        "max": 128,
                        "step": 1
                    }
                ),
                "strength": (
                    "FLOAT", {
                        "default": 1,
                        "min": 0,
                        "max": 1,
                        "step": 0.05
                    }
                ),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "process_image"
    CATEGORY = "image/HakuImg"

    def process_image(
            self,
            images: Image.Image,
            blur: int,
            strength: int,
            glow_mode: str,
    ):
        images = images.squeeze().numpy()
        images = (images * 255).astype(np.uint8)
        images = Image.fromarray(images, 'RGB').convert('RGBA')

        images = run(
            images,
            blur,
            strength,
            glow_mode
        )

        images = np.array(images).astype(np.float32) / 255.0
        images = torch.from_numpy(images)[None,]

        return (images,)
