import torch
from ..hakuimg.pixeloe import run



def image_preprocess(img: torch.Tensor, device: str):
    if img.ndim == 3:
        img = img.unsqueeze(0)
    if img.size(3) <= 4:
        img = img.permute(0, 3, 1, 2)
        use_channel_last = True
    if img.size(1) == 4:
        img = img[:, :3]
    org_device = img.device
    if device != "default":
        img = img.to(device)
    return img, use_channel_last, org_device


class PixelOE:
    INPUT_TYPES = lambda: {
        "required": {
            "pixel_size": ("INT", {"default": 4, "min": 1, "max": 32}),
            "thickness": ("INT", {"default": 2, "min": 0, "max": 6}),
            "img": ("IMAGE",),
            "mode": (["contrast", "k_centroid", "lanczos", "nearest", "bilinear"],),
            "color_quant": ("BOOLEAN", {"default": False}),
            "no_post_upscale": ("BOOLEAN", {"default": False}),
            "num_colors": ("INT", {"default": 256, "min": 2, "max": 256}),
            "quant_mode": (["kmeans", "weighted-kmeans", "repeat-kmeans"],),
            "dither_mode": (["ordered", "error_diffusion", "none"],),
            "device": (["default", "cpu", "cuda", "mps"],),
        },
    }
    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE")
    RETURN_NAMES = (
        "pixel_image",
        "oe_image",
        "oe_weight",
    )
    FUNCTION = "execute"
    CATEGORY = "image/HakuImg"

    def execute(
        self,
        pixel_size: int,
        thickness: int,
        img: torch.Tensor,
        mode: str,
        color_quant: bool,
        no_post_upscale: bool,
        num_colors: int,
        quant_mode: str,
        dither_mode: str,
        device: str,
    ):
        result, oe_image, oe_weight = run(
            pixel_size=pixel_size,
            thickness=thickness,
            img=img,
            mode=mode,
            color_quant=color_quant,
            no_post_upscale=no_post_upscale,
            num_colors=num_colors,
            quant_mode=quant_mode,
            dither_mode=dither_mode,
            device=device,
        )

        return result, oe_image, oe_weight
