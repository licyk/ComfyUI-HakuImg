import torch
import numpy as np
from PIL import Image
from ..hakuimg.lens_distortion import run



class LENDISTORTION:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
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
            image: Image.Image,
            lens_distortion_k1: float,
            lens_distortion_k2: float,
    ):
        image = image.squeeze().numpy()
        image = (image * 255).astype(np.uint8)
        image = Image.fromarray(image, 'RGB').convert('RGBA')

        image = run(
            image,
            lens_distortion_k1,
            lens_distortion_k2,
        )

        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image,)
