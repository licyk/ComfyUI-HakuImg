from typing import Any

import torch
import numpy as np
from PIL import Image
from ..effects.lens_distortion import run



class LENDISTORTION:
    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
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
            image: torch.Tensor,
            lens_distortion_k1: float,
            lens_distortion_k2: float,
    ) -> tuple[torch.Tensor]:
        image_tensor = image.squeeze().numpy()
        image_tensor = (image_tensor * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_tensor, 'RGB').convert('RGBA')

        image_pil = run(
            image_pil,
            lens_distortion_k1,
            lens_distortion_k2,
        )

        image_output = np.array(image_pil).astype(np.float32) / 255.0
        image_output = torch.from_numpy(image_output)[None,]

        return (image_output,)
