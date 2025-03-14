import torch


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
