import torch
import numpy as np
from PIL import Image
from ..hakuimg.sketch import run


class SKETCH:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "kernel_size": (
                    "INT", {
                        "default": 0,
                        "min": 0,
                        "max": 1024,
                        "step": 0.05
                    }
                ),
                "sigma": (
                    "FLOAT", {
                        "default": 1.4,
                        "min": 0,
                        "max": 1024,
                        "step": 0.05
                    }
                ),
                "k_sigma": (
                    "FLOAT", {
                        "default": 1.6,
                        "min": 0,
                        "max": 1024,
                        "step": 0.05
                    }
                ),
                "epsilon": (
                    "FLOAT", {
                        "default": -0.03,
                        "min": -1,
                        "max": 1,
                        "step": 0.005
                    }
                ),
                "phi": (
                    "FLOAT", {
                        "default": 10,
                        "min": 0,
                        "max": 1024,
                        "step": 1
                    }
                ),
                "gamma": (
                    "FLOAT", {
                        "default": 1.0,
                        "min": 0,
                        "max": 1024,
                        "step": 0.005
                    }
                ),
                "color_mode": (
                    [
                        "gray",
                        "rgb"
                    ],
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
            kernel_size: float,
            sigma: float,
            k_sigma: float,
            epsilon: float,
            phi: float,
            gamma: float,
            color_mode: str
    ):
        images = images.squeeze().numpy()
        images = (images * 255).astype(np.uint8)
        images = Image.fromarray(images, 'RGB').convert('RGBA')

        images = run(
            images,
            kernel_size,
            sigma,
            k_sigma,
            epsilon,
            phi,
            gamma,
            color_mode
        )

        images = np.array(images).astype(np.float32) / 255.0
        images = torch.from_numpy(images)[None,]

        return (images,)
