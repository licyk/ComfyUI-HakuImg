import torch
import numpy as np
from PIL import Image
from ..hakuimg.pixel import run



class PIXELIZE:
    @classmethod
    def INPUT_TYPES(cls):
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
            image: Image.Image,
            colors: int,
            dot_size: int,
            outline: int,
            smooth: int,
            mode: str,
            precise: int,
            resize: bool,
        ):
        image = image.squeeze().numpy()
        image = (image * 255).astype(np.uint8)
        image = Image.fromarray(image, 'RGB').convert('RGBA')

        image = run(
            image,
            colors,
            dot_size,
            outline,
            smooth,
            mode,
            precise,
            resize,
        )

        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image,)
