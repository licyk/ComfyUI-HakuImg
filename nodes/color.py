import torch
import numpy as np
from PIL import Image
from ..hakuimg.color import run


class COLOR:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "temperature": (
                    "INT", {
                        "default": 0,
                        "min": -100,
                        "max": 100,
                        "step": 1
                    }
                ),
                "hue": (
                    "INT", {
                        "default": 0,
                        "min": -90,
                        "max": 90,
                        "step": 1
                    }
                ),
                "brightness": (
                    "INT", {
                        "default": 0,
                        "min": -100,
                        "max": 100,
                        "step": 1
                    }
                ),
                "contrast": (
                    "INT", {
                        "default": 0,
                        "min": -100,
                        "max": 100,
                        "step": 1
                    }
                ),
                "saturation": (
                    "INT", {
                        "default": 0,
                        "min": -100,
                        "max": 100,
                        "step": 1
                    }
                ),
                "gamma": (
                    "FLOAT", {
                        "default": 1,
                        "min": 0.2,
                        "max": 2.2,
                        "step": 0.1
                    }
                ),
                "exposure_offset": (
                    "FLOAT", {
                        "default": 0,
                        "min": 0,
                        "max": 1,
                        "step": 0.01
                    }
                ),
                "vignette": (
                    "FLOAT", {
                        "default": 0,
                        "min": 0,
                        "max": 1,
                        "step": 0.01
                    }
                ),
                "noise": (
                    "FLOAT", {
                        "default": 0,
                        "min": 0,
                        "max": 1,
                        "step": 0.01
                    }
                ),
                "sharpness": (
                    "FLOAT", {
                        "default": 0,
                        "min": 0,
                        "max": 1,
                        "step": 0.01
                    }
                ),
                "hdr": (
                    "FLOAT", {
                        "default": 0,
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
            images: Image.Image,
            temperature: int,
            hue: int,
            brightness: int,
            contrast: int,
            saturation: int,
            gamma: float,
            exposure_offset: float,
            vignette: float,
            noise: float,
            sharpness: float,
            hdr: float,
    ):
        images = images.squeeze().numpy()
        images = (images * 255).astype(np.uint8)
        images = Image.fromarray(images, 'RGB').convert('RGBA')

        images = run(
            images,
            brightness,
            contrast,
            saturation,
            temperature,
            hue,
            gamma,
            exposure_offset,
            hdr,
            noise,
            sharpness,
            vignette
        )

        images = np.array(images).astype(np.float32) / 255.0
        images = torch.from_numpy(images)[None,]

        return (images,)
