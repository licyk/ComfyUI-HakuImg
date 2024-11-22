import torch
import numpy as np
from PIL import Image
from ..hakuimg.lens_distortion import run


class TILTSHIFT:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
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
            image: Image.Image,
            tilt_shift_focus_ratio: float,
            tilt_shift_dof: int,
    ):
        image = image.squeeze().numpy()
        image = (image * 255).astype(np.uint8)
        image = Image.fromarray(image, 'RGB').convert('RGBA')

        image = run(
            image,
            tilt_shift_focus_ratio,
            tilt_shift_dof,
        )

        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image,)
