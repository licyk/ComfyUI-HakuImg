import torch
from pixeloe.torch.pixelize import pixelize
from .image_preprocess import image_preprocess


def run(
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
    img, use_channel_last, org_device = image_preprocess(img, device)
    result, oe_image, oe_weight = pixelize(
        img,
        pixel_size,
        thickness,
        mode,
        do_color_match=True,
        do_quant=color_quant,
        num_colors=num_colors,
        quant_mode=quant_mode,
        dither_mode=dither_mode,
        no_post_upscale=no_post_upscale,
        return_intermediate=True,
    )
    if oe_weight is not None:
        oe_weight = oe_weight.to(org_device).repeat(1, 3, 1, 1)
    else:
        oe_weight = torch.zeros_like(result)
    if oe_image is None:
        oe_image = torch.zeros_like(result)
    result = result.to(org_device)
    oe_image = oe_image.to(org_device)
    if use_channel_last:
        result = result.permute(0, 2, 3, 1)
        oe_image = oe_image.permute(0, 2, 3, 1)
        if oe_weight is not None:
            oe_weight = oe_weight.permute(0, 2, 3, 1)
    return result, oe_image, oe_weight
