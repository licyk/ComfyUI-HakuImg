import torch
import numpy as np
from PIL import Image
from ..hakuimg.custom_exif import run



class CUSTOMEXIF:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "custom_exif": (
                    "STRING", {
                        "default": "",
                        "multiline": True
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
            custom_exif: str,
    ):
        image = image.squeeze().numpy()
        image = (image * 255).astype(np.uint8)
        image = Image.fromarray(image, 'RGB').convert('RGBA')

        image = run(
            image,
            custom_exif,
        )

        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image,)
