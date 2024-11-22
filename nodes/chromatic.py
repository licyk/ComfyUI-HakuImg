import torch
import numpy as np
from PIL import Image
from ..hakuimg.chromatic import run


class CHROMATIC:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "strength": (
                    "FLOAT", {
                        "default": 1,
                        "min": 0,
                        "max": 3,
                        "step": 0.05
                    }
                ),
                "blur": (
                    "BOOLEAN", {
                        "default": False
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
            strength: float,
            blur: bool,
    ):
        images = images.squeeze().numpy()
        images = (images * 255).astype(np.uint8)
        images = Image.fromarray(images, 'RGB')

        images = run(
            images,
            strength,
            blur,
        )

        images = np.array(images).astype(np.float32) / 255.0
        images = torch.from_numpy(images)[None,]

        return (images,)
