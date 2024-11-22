import torch
import numpy as np
from PIL import Image
from ..hakuimg.lens_distortion import run


class LENDISTORTION:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "lens_distortion_k1": (
                    "FLOAT", {
                        "default": 0,
                        "min": -1,
                        "max": 1,
                        "step": 0.01
                    }
                ),
                "lens_distortion_k2": (
                    "FLOAT", {
                        "default": 0,
                        "min": -1,
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
            images: Image.Image,
            lens_distortion_k1: float,
            lens_distortion_k2: float,
    ):
        images = images.squeeze().numpy()
        images = (images * 255).astype(np.uint8)
        images = Image.fromarray(images, 'RGB').convert('RGBA')

        images = run(
            images,
            lens_distortion_k1,
            lens_distortion_k2
        )

        images = np.array(images).astype(np.float32) / 255.0
        images = torch.from_numpy(images)[None,]

        return (images,)
