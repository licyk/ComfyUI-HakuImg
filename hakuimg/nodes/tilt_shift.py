from typing import Any

import torch
import numpy as np
from PIL import Image
from ..effects.lens_distortion import run


class TILTSHIFT:
    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
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
            image: torch.Tensor,
            tilt_shift_focus_ratio: float,
            tilt_shift_dof: int,
    ) -> tuple[torch.Tensor]:
        image_tensor = image.squeeze().numpy()
        image_tensor = (image_tensor * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_tensor, 'RGB').convert('RGBA')

        image_pil = run(
            image_pil,
            tilt_shift_focus_ratio,
            tilt_shift_dof,
        )

        image_output = np.array(image_pil).astype(np.float32) / 255.0
        image_output = torch.from_numpy(image_output)[None,]

        return (image_output,)
