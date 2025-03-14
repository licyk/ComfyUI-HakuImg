import torch
from torchvision.transforms.functional import to_pil_image
from pixeloe.torch.utils import pre_resize
from .image_preprocess import image_preprocess


def run(
    img: torch.Tensor,
    target_pixels: int,
    pixel_size: int,
    device: str,
):
    img, use_channel_last, org_device = image_preprocess(img, device)
    img = to_pil_image(img[0])
    img = pre_resize(img, target_size=target_pixels, patch_size=pixel_size)
    img = img.to(org_device)
    if use_channel_last:
        img = img.permute(0, 2, 3, 1)
    return (img,)
