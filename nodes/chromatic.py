import torch
import numpy as np
from PIL import Image
from ..hakuimg.chromatic import run



class CHROMATIC:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "strength": (
                    "FLOAT", {
                        "default": 1,
                        "min": 0,
                        "max": 3,
                        "step": 0.01
                    }
                ),
                "blur": (
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
            strength: float,
            blur: bool,
    ):
        image = image.squeeze().numpy()
        image = (image * 255).astype(np.uint8)
        image = Image.fromarray(image, 'RGB')

        image = run(
            image,
            strength,
            blur,
        )

        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image,)
