from typing import Any

import torch
import numpy as np
from PIL import Image
from ..effects.chromatic import run



class CHROMATIC:
    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "image": ("IMAGE",),
                "strength": (
                    "FLOAT", {
                        "default": 1,
                        "min": 0,
                        "max": 3,
                        "step": 0.01
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
            image: torch.Tensor,
            strength: float,
            blur: bool,
    ) -> tuple[torch.Tensor]:
        image_tensor = image.squeeze().numpy()
        image_tensor = (image_tensor * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_tensor, 'RGB')

        image_pil = run(
            image_pil,
            strength,
            blur,
        )

        image_output = np.array(image_pil).astype(np.float32) / 255.0
        image_output = torch.from_numpy(image_output)[None,]

        return (image_output,)
