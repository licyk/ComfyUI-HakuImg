import torch
from .image_preprocess import image_preprocess
from pixeloe.torch.outline import outline_expansion


def run(
    img: torch.Tensor,
    pixel_size: int,
    thickness: int,
    device: str,
):
    img, use_channel_last, org_device = image_preprocess(img, device)
    oe_image, oe_weight = outline_expansion(img, thickness, thickness, pixel_size)
    oe_image = oe_image.to(org_device)
    oe_weight = oe_weight.to(org_device).repeat(1, 3, 1, 1)
    if use_channel_last:
        oe_image = oe_image.permute(0, 2, 3, 1)
        oe_weight = oe_weight.permute(0, 2, 3, 1)
    return oe_image, oe_weight
