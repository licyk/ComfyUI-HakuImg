import torch
import numpy as np
from PIL import Image
from ..hakuimg.lens_distortion import run


class TILTSHIFT:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "tilt_shift_focus_ratio": (
                    "FLOAT", {
                        "default": 0,
                        "min": -3,
                        "max": 3,
                        "step": 0.5
                    }
                ),
                "tilt_shift_dof": (
                    "INT", {
                        "default": 60,
                        "min": 10,
                        "max": 100,
                        "step": 1
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
            tilt_shift_focus_ratio: float,
            tilt_shift_dof: int,
    ):
        images = images.squeeze().numpy()
        images = (images * 255).astype(np.uint8)
        images = Image.fromarray(images, 'RGB').convert('RGBA')

        images = run(
            images,
            tilt_shift_focus_ratio,
            tilt_shift_dof
        )

        images = np.array(images).astype(np.float32) / 255.0
        images = torch.from_numpy(images)[None,]

        return (images,)
