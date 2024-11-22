import torch
import numpy as np
from PIL import Image
from ..inoutpaint.main import run


class INOUTPAINT:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
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
            images: Image.Image,
            width: int,
            height: int,
            align_top: int,
            align_left: int,
            align_bottom: int,
            align_right: int,
    ):
        images = images.squeeze().numpy()
        images = (images * 255).astype(np.uint8)
        images = Image.fromarray(images, 'RGB').convert('RGBA')

        images, _, _ = run(
            images,
            width,
            height,
            align_top,
            align_bottom,
            align_left,
            align_right,
        )

        images = np.array(images).astype(np.float32) / 255.0
        images = torch.from_numpy(images)[None,]

        return (images,)
