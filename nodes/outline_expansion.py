import torch
from ..hakuimg.outline_expansion import run


class OutlineExpansion:
    INPUT_TYPES = lambda: {
        "required": {
            "img": ("IMAGE",),
            "pixel_size": ("INT", {"default": 4, "min": 1, "max": 32}),
            "thickness": ("INT", {"default": 3, "min": 1, "max": 6}),
            "device": (["default", "cpu", "cuda", "mps"],),
        },
    }
    RETURN_TYPES = ("IMAGE", "IMAGE")
    RETURN_NAMES = (
        "oe_image",
        "oe_weight",
    )
    FUNCTION = "execute"
    CATEGORY = "image/HakuImg"

    def execute(
        self,
        img: torch.Tensor,
        pixel_size: int,
        thickness: int,
        device: str,
    ):
        oe_image, oe_weight = run(
            img=img,
            pixel_size=pixel_size,
            thickness=thickness,
            device=device,
        )

        return oe_image, oe_weight