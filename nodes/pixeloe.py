import cv2
import torch
import numpy as np
from PIL import Image
from ..hakuimg.PixelOE.pixeloe.pixelize import pixelize



class PIXELOE:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "target_size": (
                    "INT", {
                        "default": 256,
                        "min": 0,
                        "max": 1024,
                        "step": 1
                    }
                ),
                "patch_size": (
                    "INT", {
                        "default": 8,
                        "min": 0,
                        "max": 1024,
                        "step": 1
                    }
                ),
                "pixel_size": (
                    "INT", {
                        "default": 0,
                        "min": 0,
                        "max": 1024,
                        "step": 1
                    }
                ),
                "thickness": (
                    "INT", {
                        "default": 2,
                        "min": 0,
                        "max": 1024,
                        "step": 1
                    }
                ),
                "colors": (
                    "INT", {
                        "default": 0,
                        "min": 0,
                        "max": 1024,
                        "step": 1
                    }
                ),
                "contrast": (
                    "FLOAT", {
                        "default": 1.0,
                        "min": 0,
                        "max": 1024,
                        "step": 0.05
                    }
                ),
                "saturation": (
                    "FLOAT", {
                        "default": 1.0,
                        "min": 0,
                        "max": 1024,
                        "step": 0.05
                    }
                ),
                "mode": (
                    [
                        "contrast",
                        "center",
                        "k-centroid",
                        "bicubic",
                        "nearest"
                    ],
                ),
                "color_quant_methon": (
                    [
                        "kmeans",
                        "maxcover"
                    ],
                ),
                "color_matching": (
                    "BOOLEAN", {
                        "default": True
                    }
                ),
                "color_with_weight": (
                    "BOOLEAN", {
                        "default": False
                    }
                ),
                "no_upscale": (
                    "BOOLEAN", {
                        "default": False
                    }
                ),
                "no_downscale": (
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
            target_size: int,
            patch_size: int,
            pixel_size: int,
            thickness: int,
            colors: int,
            contrast: float,
            saturation: float,
            mode: str,
            color_quant_methon: str,
            color_matching: bool,
            color_with_weight: bool,
            no_upscale: bool,
            no_downscale: bool,
    ):
        image = image.squeeze().numpy()
        image = (image * 255).astype(np.uint8)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        image = pixelize(
            image,
            mode,
            target_size,
            patch_size,
            pixel_size if pixel_size != 0 else None,
            thickness,
            color_matching,
            contrast,
            saturation,
            colors if colors != 0 else None,
            color_quant_methon,
            color_with_weight,
            no_upscale,
            no_downscale,
        )

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image,)
