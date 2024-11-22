import torch
import numpy as np
from PIL import Image
from ..hakuimg.pixel import run




class PIXELIZE:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "colors": (
                    "INT", {
                        "default": 16,
                        "min": 0,
                        "max": 1024,
                        "step": 1
                    }
                ),
                "dot_size": (
                    "INT", {
                        "default": 8,
                        "min": 0,
                        "max": 1024,
                        "step": 1
                    }
                ),
                "outline": (
                    "INT", {
                        "default": 0,
                        "min": 0,
                        "max": 1024,
                        "step": 1
                    }
                ),
                "smooth": (
                    "INT", {
                        "default": 5,
                        "min": 0,
                        "max": 1024,
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
            images: Image.Image,
            colors: int,
            dot_size: int,
            outline: int,
            smooth: int,
            mode: str,
            precise: int,
            resize: bool,
        ):
        images = images.squeeze().numpy()
        images = (images * 255).astype(np.uint8)
        images = Image.fromarray(images, 'RGB').convert('RGBA')

        images = run(
            images,
            colors,
            dot_size,
            outline,
            smooth,
            mode,
            precise,
            resize
        )

        images = np.array(images).astype(np.float32) / 255.0
        images = torch.from_numpy(images)[None,]

        return (images,)
