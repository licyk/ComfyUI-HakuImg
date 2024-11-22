import torch
import numpy as np
from PIL import Image
from ..hakuimg.sketch import run



class SKETCH:
    @classmethod
    def INPUT_TYPES(cls):
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
            image: Image.Image,
            kernel_size: float,
            sigma: float,
            k_sigma: float,
            epsilon: float,
            phi: float,
            gamma: float,
            color_mode: str,
            scale: bool,
    ):
        image = image.squeeze().numpy()
        image = (image * 255).astype(np.uint8)
        image = Image.fromarray(image, 'RGB').convert('RGBA')

        image = run(
            image,
            kernel_size,
            sigma,
            k_sigma,
            epsilon,
            phi,
            gamma,
            color_mode,
            scale,
        )

        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image,)
