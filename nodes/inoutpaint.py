import torch
import numpy as np
from PIL import Image
from ..inoutpaint.main import run



class INOUTPAINT:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
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
            image: Image.Image,
            width: int,
            height: int,
            align_top: int,
            align_left: int,
            align_bottom: int,
            align_right: int,
    ):
        image = image.squeeze().numpy()
        image = (image * 255).astype(np.uint8)
        image = Image.fromarray(image, 'RGB').convert('RGBA')

        image, _, _ = run(
            image,
            width,
            height,
            align_top,
            align_bottom,
            align_left,
            align_right,
        )

        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image,)
