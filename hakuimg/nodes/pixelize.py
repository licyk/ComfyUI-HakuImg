from typing import Any

import torch
import numpy as np
from PIL import Image
from ..effects.pixel import run



class PIXELIZE:
    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "image": ("IMAGE",),
                "colors": (
                    "INT", {
                        "default": 128,
                        "min": 2,
                        "max": 256,
                        "step": 1
                    }
                ),
                "dot_size": (
                    "INT", {
                        "default": 6,
                        "min": 1,
                        "max": 32,
                        "step": 1
                    }
                ),
                "outline": (
                    "INT", {
                        "default": 1,
                        "min": 0,
                        "max": 10,
                        "step": 1
                    }
                ),
                "smooth": (
                    "INT", {
                        "default": 4,
                        "min": 0,
                        "max": 10,
                        "step": 1
                    }
                ),
                "mode": (
                    [
                        "kmeans",
                        "dithering",
                        "kmeans with dithering"
                    ],
                ),
                "precise": (
                    "INT", {
                        "default": 10,
                        "min": 0,
                        "max": 1024,
                        "step": 1
                    }
                ),
                "resize": (
                    "BOOLEAN", {
                        "default": True
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
            colors: int,
            dot_size: int,
            outline: int,
            smooth: int,
            mode: str,
            precise: int,
            resize: bool,
        ) -> tuple[torch.Tensor]:
        image_array = image.squeeze().numpy()
        image_array = (image_array * 255).astype(np.uint8)

        pil_image = Image.fromarray(
            image_array,
            "RGB",
        ).convert("RGBA")

        pil_image = run(
            pil_image,
            colors,
            dot_size,
            outline,
            smooth,
            mode,
            precise,
            resize,
        )

        output_array = np.asarray(pil_image).astype(np.float32) / 255.0
        output_image = torch.from_numpy(output_array)[None,]

        return (output_image,)
