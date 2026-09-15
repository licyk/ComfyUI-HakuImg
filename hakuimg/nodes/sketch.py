from typing import Any

import torch
import numpy as np
from PIL import Image
from ..effects.sketch import run



class SKETCH:
    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "image": ("IMAGE",),
                "kernel_size": (
                    "INT", {
                        "default": 0,
                        "min": 0,
                        "max": 25,
                        "step": 1
                    }
                ),
                "sigma": (
                    "FLOAT", {
                        "default": 1.4,
                        "min": 1,
                        "max": 5,
                        "step": 0.05
                    }
                ),
                "k_sigma": (
                    "FLOAT", {
                        "default": 1.6,
                        "min": 1,
                        "max": 5,
                        "step": 0.05
                    }
                ),
                "epsilon": (
                    "FLOAT", {
                        "default": -0.03,
                        "min": -0.2,
                        "max": 0.2,
                        "step": 0.005
                    }
                ),
                "phi": (
                    "FLOAT", {
                        "default": 10,
                        "min": 1,
                        "max": 50,
                        "step": 1
                    }
                ),
                "gamma": (
                    "FLOAT", {
                        "default": 1.0,
                        "min": 0.75,
                        "max": 1,
                        "step": 0.005
                    }
                ),
                "color_mode": (
                    [
                        "gray",
                        "rgb"
                    ],
                ),
                "scale": (
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
            kernel_size: float,
            sigma: float,
            k_sigma: float,
            epsilon: float,
            phi: float,
            gamma: float,
            color_mode: str,
            scale: bool,
    ) -> tuple[torch.Tensor]:
        image_tensor = image.squeeze().numpy()
        image_tensor = (image_tensor * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_tensor, 'RGB').convert('RGBA')

        image_pil = run(
            image_pil,
            kernel_size,
            sigma,
            k_sigma,
            epsilon,
            phi,
            gamma,
            color_mode,
            scale,
        )

        image_output = np.array(image_pil).astype(np.float32) / 255.0
        image_output = torch.from_numpy(image_output)[None,]

        return (image_output,)
