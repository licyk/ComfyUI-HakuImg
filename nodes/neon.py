import torch
import numpy as np
from PIL import Image
from ..hakuimg.neon import run



class NEON:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
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
                        "step": 0.01
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
            image: Image.Image,
            blur: int,
            strength: int,
            glow_mode: str,
    ):
        image = image.squeeze().numpy()
        image = (image * 255).astype(np.uint8)
        image = Image.fromarray(image, 'RGB').convert('RGBA')

        image = run(
            image,
            blur,
            strength,
            glow_mode,
        )

        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image,)
