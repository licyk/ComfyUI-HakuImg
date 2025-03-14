import torch
from ..hakuimg.pre_resize import run


class PreResize:
    INPUT_TYPES = lambda: {
        "required": {
            "img": ("IMAGE",),
            "target_pixels": ("INT", {"default": 256, "min": 1, "max": 1024}),
            "pixel_size": ("INT", {"default": 4, "min": 1, "max": 32}),
            "device": (["default", "cpu", "cuda", "mps"],),
        },
    }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("img",)
    FUNCTION = "execute"
    CATEGORY = "image/HakuImg"

    def execute(
        self,
        img: torch.Tensor,
        target_pixels: int,
        pixel_size: int,
        device: str,
    ):
        img = run(
            img=img,
            target_pixels=target_pixels,
            pixel_size=pixel_size,
            device=device,
        )

        return img
