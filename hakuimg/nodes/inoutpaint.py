from typing import Any

import torch
import numpy as np
from PIL import Image
from ..effects.inoutpaint.main import run



class INOUTPAINT:
    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "image": ("IMAGE",),
                "width": (
                    "INT", {
                        "default": 512,
                        "step": 1
                    }
                ),
                "height": (
                    "INT", {
                        "default": 512,
                        "step": 1
                    }
                ),
                "align_top": (
                    "INT", {
                        "default": 0,
                        "step": 1
                    }
                ),
                "align_left": (
                    "INT", {
                        "default": 0,
                        "step": 1
                    }
                ),
                "align_bottom": (
                    "INT", {
                        "default": 512,
                        "step": 1
                    }
                ),
                "align_right": (
                    "INT", {
                        "default": 512,
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
            width: int,
            height: int,
            align_top: int,
            align_left: int,
            align_bottom: int,
            align_right: int,
    ) -> tuple[torch.Tensor]:
        image_array = image.squeeze().numpy()
        image_array = (image_array * 255).astype(np.uint8)

        pil_image = Image.fromarray(
            image_array,
            "RGB",
        ).convert("RGBA")

        pil_image, _, _ = run(
            pil_image,
            width,
            height,
            align_top,
            align_bottom,
            align_left,
            align_right,
        )

        output_array = np.array(pil_image).astype(np.float32) / 255.0
        output_image = torch.from_numpy(output_array)[None,]

        return (output_image,)
