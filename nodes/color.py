import torch
import numpy as np
from PIL import Image
from ..hakuimg.color import run



class COLOR:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
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
            image: Image.Image,
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
        image = image.squeeze().numpy()
        image = (image * 255).astype(np.uint8)
        image = Image.fromarray(image, 'RGB').convert('RGBA')

        image = run(
            image,
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
            vignette,
        )

        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image,)
