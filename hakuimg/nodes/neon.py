from typing import Any

import torch
import numpy as np
from PIL import Image
from ..effects.neon import run



class NEON:
    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
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
            image: torch.Tensor,
            blur: int,
            strength: int,
            glow_mode: str,
    ) -> tuple[torch.Tensor]:
        image_tensor = image.squeeze().numpy()
        image_tensor = (image_tensor * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_tensor, 'RGB').convert('RGBA')

        image_pil = run(
            image_pil,
            blur,
            strength,
            glow_mode,
        )

        image_output = np.array(image_pil).astype(np.float32) / 255.0
        image_output = torch.from_numpy(image_output)[None,]

        return (image_output,)
